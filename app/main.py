import pydantic
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastui import AnyComponent, FastUI
from fastui import components as c, prebuilt_html
from fastui.components.display import DisplayLookup, DisplayMode
from fastui.events import BackEvent, GoToEvent
from pydantic import BaseModel, Field, TypeAdapter
import json
from pathlib import Path

app = FastAPI()


class City(BaseModel):
    id: int
    city: str = Field(title="Name")
    city_ascii: str = Field(title="City Ascii")
    lat: float = Field(title="Latitude")
    lng: float = Field(title="Longitude")
    country: str = Field(title="Country")
    iso2: str = Field(title="ISO2")
    iso3: str = Field(title="ISO3")
    admin_name: str = Field(title="Admin Name")
    capital: str = Field(title="Capital")
    population: float = Field(title="Population")


def cities_list():
    cities_file = Path(__file__).parent / "cities.json"
    with open(cities_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    cities = [City(**city) for city in data]
    return cities


print(cities_list())


@app.get("/api/cities", response_model=FastUI, response_model_exclude_none=True)
def cities_view(page: int = 1, country=None):
    cities = cities_list()
    page_size = 10
    filter_form_initial = {}
    return c.Page(
        components=[
            c.Table(
                data=cities[(page - 1) * page_size : page * page_size],
                data_model=City,
                columns=[
                    DisplayLookup(
                        field="city",
                        on_click=GoToEvent(url="./{id}"),
                        table_width_percent=33,
                    ),
                    DisplayLookup(field="country", table_width_percent=33),
                    DisplayLookup(field="population", table_width_percent=33),
                ],
            ),
            c.Pagination(page=page, page_size=page_size, total=len(cities)),
        ]
    )


@app.get("/{path:path}")
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title="FastUI Demo"))
