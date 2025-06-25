from sqlalchemy import select, desc
from app.core.Database import SessionLocal
from app.models.market import PollingJob
from app.core.logging import logger as logging
from datetime import datetime
import asyncio
import httpx


class PollingService:
    def __init__(self):
        self.poll = False
        self.last_run = {}

    async def start_polling(self):
        self.poll = True
        async with SessionLocal() as db:
            while self.poll:
                result = await db.execute(
                    select(
                        PollingJob.symbols,
                        PollingJob.provider,
                        PollingJob.id,
                        PollingJob.interval,
                    ).where(PollingJob.status == "accepted")
                )
                jobs = result.fetchall()
                for job in jobs:
                    if job[2]:
                        if job[2] not in self.last_run:
                            self.last_run[job[2]] = datetime.now()

                        time_difference = datetime.now() - self.last_run[job[2]]
                        if time_difference.total_seconds() >= job[3]:
                            for symbol in job[0].get("symbols", []):
                                logging.debug(
                                        f"Running poll: {job[2]} for symbol: {symbol}, provider: {job[1]}"
                                    )
                                res = await self._call_own_endpoint(symbol, job[1])
                                if not res:
                                    logging.info(
                                        f"Failed to poll {job[2]} for symbol: {symbol}, provider: {job[1]}"
                                    )
                                    
                            self.last_run[job[2]] = datetime.now()

                await asyncio.sleep(5)

    def stop_polling(self):
        self.poll = False

    async def _call_own_endpoint(self, symbol: str, provider: str):
        async with httpx.AsyncClient() as client:
            # Replace with your actual endpoint and parameters
            response = await client.get(
                "http://localhost:8000/prices/latest/",
                params={"symbol": symbol, "provider": provider},
                follow_redirects=True, timeout=5
            )
            data = response.status_code
            if data != 200:
                return False

            return True
