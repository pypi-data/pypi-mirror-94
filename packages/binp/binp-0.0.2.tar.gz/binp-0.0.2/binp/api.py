from os import getenv
from pathlib import Path
from time import monotonic
from typing import List

from fastapi import FastAPI, HTTPException, Response
from fastapi.staticfiles import StaticFiles
from pydantic.main import BaseModel

from binp.action import ActionInfo, Action
from binp.journals import Headline, Journal, Journals
from binp.kv import KV


class InvokeResult(BaseModel):
    name: str
    duration: float


def create_app(journals: Journals, kv: KV, actions: Action) -> FastAPI:
    internal = FastAPI(title='PYRED', description='Internal APIs')

    @internal.get('/actions/', operation_id='listActions', response_model=List[ActionInfo])
    async def list_actions():
        return actions.actions

    @internal.post('/action/{name}', operation_id='invokeAction', response_model=InvokeResult)
    async def invoke_action(name: str):
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

    @internal.get("/journal/{journal_id}", operation_id='getJournal', response_model=Journal)
    async def get_journal(journal_id: int):
        """
        Get single journal record by ID. If no record found - 404 returned.
        """
        res = await journals.get(journal_id)
        if res is None:
            raise HTTPException(status_code=404, detail=f'journal {journal_id} not found')
        return res

    static_dir = Path(__file__).absolute().parent / "static"
    app = FastAPI(title='PYRED', description='User defined APIs. See internal APIs <a href="internal/redoc">here</a>')
    if getenv('DEV', '') == 'true':
        from fastapi.middleware.cors import CORSMiddleware

        origins = [
            "http://localhost",
            "http://localhost:8000",
            "http://localhost:5000",
        ]

        app.add_middleware(
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
