from asyncio import Queue
from os import getenv
from pathlib import Path
from time import monotonic
from typing import List

from fastapi import FastAPI, HTTPException, Response, WebSocket
from fastapi.staticfiles import StaticFiles
from pydantic.main import BaseModel
from websockets import ConnectionClosed

from binp.action import ActionInfo, Action
from binp.journals import Headline, Journal, Journals
from binp.kv import KV
from binp.service import Info, Service


class InvokeResult(BaseModel):
    name: str
    duration: float


class ServiceControl(BaseModel):
    running: bool


def create_app(journals: Journals, kv: KV, actions: Action, services: Service) -> FastAPI:
    internal = FastAPI(title='BINP', description='Internal APIs')

    @internal.get('/actions/', operation_id='listActions', response_model=List[ActionInfo])
    async def list_actions():
        """
        List available actions
        """
        return actions.actions

    @internal.post('/action/{name}', operation_id='invokeAction', response_model=InvokeResult)
    async def invoke_action(name: str):
        """
        Invoke custom action (methods annotated by @action)
        """
        a = monotonic()
        executed = await actions.invoke(name)
        b = monotonic()
        if not executed:
            raise HTTPException(status_code=404, detail=f'action {name} not found')
        return InvokeResult(name=name, duration=b - a)

    @internal.get("/journals/", operation_id='listJournals', response_model=List[Headline])
    async def list_journals(page: int = 0):
        """
        List journal records in reverse order. Maximum 20 items per page.
        """
        return await journals.history(page * 20)

    @internal.websocket("/journals/updates")
    async def notify_journals_updates(websocket: WebSocket):
        """
        Stream over websocket all journals headlines updates
        """
        await websocket.accept()
        with journals.journal_updated.subscribe() as queue:
            while True:
                journal_id = await queue.get()
                journal = await journals.get(journal_id)
                try:
                    await websocket.send_text(journal.json())
                except ConnectionClosed:
                    break

    @internal.get("/journal/{journal_id}", operation_id='getJournal', response_model=Journal)
    async def get_journal(journal_id: int):
        """
        Get single journal record by ID. If no record found - 404 returned.
        """
        res = await journals.get(journal_id)
        if res is None:
            raise HTTPException(status_code=404, detail=f'journal {journal_id} not found')
        return res

    @internal.websocket("/journal/{journal_id}/updates")
    async def notify_journal_updates(journal_id: int, websocket: WebSocket):
        """
        Stream over websocket single journal updates
        """
        await websocket.accept()
        queue: Queue[int] = Queue()
        with journals.record_added.subscribe(queue), journals.journal_updated.subscribe(queue):
            while True:
                event_journal_id = await queue.get()
                if event_journal_id != journal_id:
                    continue
                journal = await journals.get(journal_id)
                try:
                    await websocket.send_text(journal.json())
                except ConnectionClosed:
                    break

    @internal.get("/services/", operation_id='listServices', response_model=List[Info])
    async def list_services():
        """
        List all defined services
        """
        return services.services

    @internal.websocket("/services/updates")
    async def notify_services_updates(websocket: WebSocket):
        """
        Stream services updates
        """
        await websocket.accept()
        with services.service_changed.subscribe() as queue:
            while True:
                update = await queue.get()
                try:
                    await websocket.send_text(update.json())
                except ConnectionClosed:
                    break

    @internal.put("/service/{name}", operation_id='manageService')
    async def manage_service(name: str, control: ServiceControl):
        if control.running:
            services.start(name)
        else:
            services.stop(name)

    static_dir = Path(__file__).absolute().parent / "static"
    app = FastAPI(title='BINP', description='User defined APIs. See internal APIs <a href="internal/redoc">here</a>')
    if getenv('DEV', '') == 'true':
        from fastapi.middleware.cors import CORSMiddleware

        origins = [
            "http://localhost",
            "http://localhost:8000",
            "http://localhost:5000",
            "http://127.0.0.1:5000",
        ]

        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        internal.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    else:
        @app.get("/")
        async def main_page_redirect():
            """
            Redirects to UI
            """
            return Response(status_code=302, headers={
                'Location': 'static/index.html#/'
            })

        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    app.mount('/internal/', internal)
    return app
