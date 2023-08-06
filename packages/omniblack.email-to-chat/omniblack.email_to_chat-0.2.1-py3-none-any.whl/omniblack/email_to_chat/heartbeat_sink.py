from asyncio import create_task, get_running_loop
from datetime import datetime, timedelta, date, time
from .async_utils import run_in_executor
from pathlib import Path
from .abc import InputSink, LocalMessage, MessageType
from logging import getLogger

log = getLogger(__name__)

data_path = Path('/var/lib/omniblack_notifier/last_heartbeat')


@run_in_executor
def load_heartbeat():
    try:
        with data_path.open('r') as data_file:
            return datetime.fromisoformat(data_file.read().strip())
    except FileNotFoundError:
        return None
    except ValueError:
        log.error('Bad last heartbeat')
        return None


@run_in_executor
def write_heartbeat():
    with data_path.open('w') as data_file:
        data_file.write(datetime.now().isoformat())


nine_oclock = time(hour=9, minute=0)


class HeartBeat(InputSink):
    running_timer = None

    async def start(self):
        self.loop = get_running_loop()
        last_heartbeat = await load_heartbeat()
        if last_heartbeat is None:
            return self.run_today()

        now = datetime.now()
        diff = now - last_heartbeat

        if diff.days != 0:
            # if it has been more than 1 days since the last heartbeat
            # run today
            self.run_today()
        else:
            # we already ran today so run again tomorrow
            self.run_tomorrow()

    def run_heart_beat(self):
        create_task(self._run_heart_beat(), name='Notifier heartbeat')

    async def _run_heart_beat(self):
        log.info('Running heartbeat')
        msg = LocalMessage(
            type=MessageType.heartbeat,
            program='@omniblack/notifier',
            body='@omniblack/notifier is online and working',
        )
        await self.queue.put(msg)
        await write_heartbeat()
        self.run_tomorrow()

    def run_at(self, run_time: datetime):
        log.info(f'Next heartbeat scheduled for {run_time}')
        delay_delta = run_time - datetime.now()
        delay = delay_delta.total_seconds()

        self.running_timer = self.loop.call_later(delay, self.run_heart_beat)

    async def stop(self):
        if self.running_timer:
            self.running_timer.cancel()

    def run_today(self):
        now = datetime.now()
        if now.hour > 9:
            self.run_heart_beat()
        else:
            today = date.today()
            run_time = datetime.combine(date=today, time=nine_oclock)
            self.run_at(run_time)

    def run_tomorrow(self):
        tomorrow = date.today() + timedelta(days=1)
        next_run = datetime.combine(date=tomorrow, time=nine_oclock)
        self.run_at(next_run)
