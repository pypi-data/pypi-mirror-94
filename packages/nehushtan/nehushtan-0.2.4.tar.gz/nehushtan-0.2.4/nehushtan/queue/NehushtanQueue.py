import os
import time
from multiprocessing import Process

from nehushtan.queue.NehushtanQueueDelegate import NehushtanQueueDelegate
from nehushtan.queue.NehushtanQueueTask import NehushtanQueueTask
from nehushtan.queue.situation.NoNextTaskSituation import NoNextTaskSituation


class NehushtanQueue:
    def __init__(self, delegate: NehushtanQueueDelegate):
        self.delegate: NehushtanQueueDelegate = delegate
        self.current_workers = {}

    def get_logger(self):
        return self.delegate.logger

    def get_pool_capacity(self) -> int:
        """
        How many processes could run in the same time.
        Decided by the delegate
        """
        return self.delegate.read_config_of_delegate((NehushtanQueueDelegate.CONFIG_KEY_POOL_CAPACITY,), 1)

    def _scan_workers(self):
        """
        Scan registered workers, and remove dead ones from dictionary.
        Finally return the total running processes count.
        """
        if len(self.current_workers.items()) > 0:
            delete_keys = []
            for task_id, task_process in self.current_workers.items():
                if not task_process.is_alive():
                    self.get_logger().warning(f'Worker Process for task [{task_id}] Dead', {'pid': task_process.pid})
                    self.delegate.when_worker_process_confirmed_dead(
                        task_id,
                        {'pid': task_process.pid, 'exitcode': task_process.exitcode}
                    )
                    delete_keys.append(task_id)
            for delete_key in delete_keys:
                del self.current_workers[delete_key]
                self.get_logger().debug('remove removable finished tasks', {'task_id': delete_key})

        return len(self.current_workers.items())

    def _terminate_worker_process_of_task(self, task_reference):
        p = self.current_workers.get(task_reference)
        if p:
            p.kill()
            self.get_logger().info(
                'NehushtanQueue._terminate_worker_process_of_task done',
                {'task': task_reference, 'pid': p.pid, 'exitcode': p.exitcode, 'is_alive': p.is_alive()}
            )
            self.delegate.when_killed_worker_process(task_reference)
        else:
            self.get_logger().warning(
                'NehushtanQueue._terminate_worker_process_of_task target task not found amongst current workers',
                {'task': task_reference}
            )
            self.delegate.when_killed_worker_process(task_reference, not_found=True)

    def _loop_maintain(self, wait_till_processes_become_less_than: int = 0):
        self._scan_workers()

        self.delegate.handle_command_queue()

        kill_list = self.delegate.should_kill_any_worker_processes()
        if len(kill_list) > 0:
            for kill_task_id in kill_list:
                self._terminate_worker_process_of_task(kill_task_id)

        total_alive_current_workers = self._scan_workers()

        if wait_till_processes_become_less_than > 0:
            # need to do some wait
            if total_alive_current_workers >= wait_till_processes_become_less_than:
                time.sleep(2)
                return self._loop_maintain(wait_till_processes_become_less_than)
        else:
            return total_alive_current_workers

    def loop(self):
        self.delegate.when_loop_starts()

        while True:
            try:
                # 1. check current workers status
                total_current_workers = len(self.current_workers.items())
                self.get_logger().info('Current workers totally count', {'total': total_current_workers})

                # 2. handle command queue and kill list
                self._loop_maintain()

                # 3. check elihu command
                self.delegate.read_latest_command()
                if self.delegate.should_terminate():
                    if self.delegate.should_wait_for_all_workers_before_terminating():
                        self._loop_maintain(1)
                    break

                # 4. check queue if new task there
                if not self.delegate.is_runnable():
                    self.delegate.when_loop_should_not_run()
                    continue

                total_current_workers = len(self.current_workers.items())
                if total_current_workers >= self.get_pool_capacity():
                    self._loop_maintain(self.get_pool_capacity())

                try:
                    task = self.delegate.check_next_task()

                    if task.is_exclusive():
                        # now daemon should wait for the other tasks to be over
                        self._loop_maintain(1)
                        pass

                    if not task.before_execute():
                        self.delegate.when_task_not_executable(task)
                        continue

                    p = Process(target=NehushtanQueue.embedded_task_execute, args=(task, self.delegate))
                    p.start()
                    self.current_workers[task.get_task_reference()] = p

                    self.delegate.when_worker_process_created(
                        task.get_task_reference(),
                        f'Task [{task.get_task_reference()}] -> Process {p.name} PID is [{p.pid}]'
                    )

                except NoNextTaskSituation:
                    self.delegate.when_no_task_to_do()
                    continue

            except Exception as loop_round_error:
                self.delegate.when_loop_reports_error(loop_round_error.__str__())

        self.delegate.when_loop_terminates()

    @staticmethod
    def embedded_task_execute(embedded_task: NehushtanQueueTask, delegate: NehushtanQueueDelegate):
        """
        This works in WORKER
        """
        delegate.when_to_execute_task(embedded_task, os.getpid())
        try:
            embedded_task.execute()
        except Exception as e:
            delegate.when_task_raised_exception(embedded_task, e)
        delegate.when_task_executed(embedded_task, os.getpid())
