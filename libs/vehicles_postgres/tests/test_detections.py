from typing import Any
import uuid
import pytest

from pydantic import BaseSettings

from indexer.vehicles.entities import Detection
from indexer.vehicles.exceptions import IntegrityError

from indexer.pgvehicles import db
from indexer.pgvehicles.models import VehiclesManager


class Settings(BaseSettings):
    vehicles_db_connection: str


@pytest.fixture(scope="session")
def get_db():
    s = Settings()
    return db.DB(s.vehicles_db_connection)


@pytest.fixture(scope="session")
def vehicles_manager(get_db):
    return VehiclesManager(get_db)


@pytest.fixture(scope="session")
def vehicles():
    return [
        {'Year': 2004, 'Make': 'Toyota', 'Model': 'MR2', 'Category': 'Convertible'},
        {'Year': 2004, 'Make': 'Jeep', 'Model': 'Liberty', 'Category': 'SUV'},
        {'Year': 2015, 'Make': 'Chevrolet', 'Model': 'Silverado 2500 HD Crew Cab', 'Category': 'Pickup'},
        {'Year': 1992, 'Make': 'Ford', 'Model': 'F150 Super Cab', 'Category': 'Pickup'},
        {'Year': 1995, 'Make': 'GMC', 'Model': '3500 Club Coupe', 'Category': 'Pickup'},
        {'Year': 2005, 'Make': 'Nissan', 'Model': 'Titan Crew Cab', 'Category': 'Pickup'},
        {'Year': 1995, 'Make': 'Mitsubishi', 'Model': '3000GT', 'Category': 'Convertible, Hatchback'},
        {'Year': 2019, 'Make': 'Genesis', 'Model': 'G80', 'Category': 'Sedan'},
        {'Year': 1999, 'Make': 'Saab', 'Model': '3-Sep', 'Category': 'Hatchback, Convertible'},
        {'Year': 2020, 'Make': 'Audi', 'Model': 'A7', 'Category': 'Sedan'},
        {'Year': 1998, 'Make': 'Jaguar', 'Model': 'XJ', 'Category': 'Sedan'},
        {'Year': 1998, 'Make': 'Buick', 'Model': 'Regal', 'Category': 'Sedan'},
        {'Year': 1996, 'Make': 'MAZDA', 'Model': '626', 'Category': 'Sedan'},
        {'Year': 2010, 'Make': 'Volkswagen', 'Model': 'CC', 'Category': 'Sedan'},
        {'Year': 2005, 'Make': 'Ford', 'Model': 'E150 Super Duty Passenger', 'Category': 'Van/Minivan'},
        {'Year': 2002, 'Make': 'Mercedes-Benz', 'Model': 'M-Class', 'Category': 'SUV'},
        {'Year': 2007, 'Make': 'Mercury', 'Model': 'Mountaineer', 'Category': 'SUV'},
        {'Year': 2020, 'Make': 'Lincoln', 'Model': 'MKZ', 'Category': 'Sedan'},
        {'Year': 2002, 'Make': 'Chevrolet', 'Model': 'S10 Crew Cab', 'Category': 'Pickup'},
        {'Year': 2004, 'Make': 'Chrysler', 'Model': 'PT Cruiser', 'Category': 'Wagon'},
        {'Year': 2014, 'Make': 'BMW', 'Model': 'X6', 'Category': 'SUV'},
        {'Year': 2012, 'Make': 'Toyota', 'Model': 'Tundra Regular Cab', 'Category': 'Pickup'},
        {'Year': 1998, 'Make': 'Mercedes-Benz', 'Model': 'CL-Class', 'Category': 'Coupe'},
        {'Year': 2005, 'Make': 'Honda', 'Model': 'Element', 'Category': 'SUV'},
        {'Year': 2000, 'Make': 'Isuzu', 'Model': 'Trooper', 'Category': 'SUV'},
        {'Year': 1998, 'Make': 'Nissan', 'Model': '200SX', 'Category': 'Coupe'},
        {'Year': 2002, 'Make': 'Ford', 'Model': 'Ranger Super Cab', 'Category': 'Pickup'},
        {'Year': 2016, 'Make': 'Chevrolet', 'Model': 'Silverado 2500 HD Double Cab', 'Category': 'Pickup'},
        {'Year': 2011, 'Make': 'Ferrari', 'Model': '599 GTB Fiorano', 'Category': 'Coupe'},
        {'Year': 1999, 'Make': 'Ford', 'Model': 'Ranger Regular Cab', 'Category': 'Pickup'},
        {'Year': 2015, 'Make': 'Ford', 'Model': 'F250 Super Duty Super Cab', 'Category': 'Pickup'},
        {'Year': 2003, 'Make': 'GMC', 'Model': 'Sierra 1500 HD Crew Cab', 'Category': 'Pickup'},
        {'Year': 1995, 'Make': 'Toyota', 'Model': '4Runner', 'Category': 'SUV'},
        {'Year': 2016, 'Make': 'Ram', 'Model': 'ProMaster City', 'Category': 'Van/Minivan'},
        {'Year': 1999, 'Make': 'Suzuki', 'Model': 'Vitara', 'Category': 'SUV'},
        {'Year': 2000, 'Make': 'Acura', 'Model': 'NSX', 'Category': 'Coupe, Convertible'},
        {'Year': 2017, 'Make': 'Freightliner', 'Model': 'Sprinter 3500XD Cargo', 'Category': 'Van/Minivan'},
        {'Year': 2018, 'Make': 'Kia', 'Model': 'Soul', 'Category': 'Wagon'},
        {'Year': 2012, 'Make': 'Toyota', 'Model': 'Tundra CrewMax', 'Category': 'Pickup'},
        {'Year': 1999, 'Make': 'Chrysler', 'Model': 'Town & Country', 'Category': 'Van/Minivan'},
        {'Year': 2018, 'Make': 'Alfa Romeo', 'Model': 'Stelvio', 'Category': 'SUV'},
        {'Year': 2020, 'Make': 'Lexus', 'Model': 'LS', 'Category': 'Sedan'},
        {'Year': 1995, 'Make': 'Chevrolet', 'Model': 'Sportvan G20', 'Category': 'Van/Minivan'},
        {'Year': 1994, 'Make': 'Suzuki', 'Model': 'Swift', 'Category': 'Sedan, Hatchback'},
        {'Year': 2015, 'Make': 'Scion', 'Model': 'tC', 'Category': 'Coupe'},
        {'Year': 2001, 'Make': 'Chevrolet', 'Model': 'Suburban 2500', 'Category': 'SUV'},
        {'Year': 1995, 'Make': 'Dodge', 'Model': 'Viper', 'Category': 'Convertible'},
        {'Year': 2011, 'Make': 'Ram', 'Model': 'Dakota Crew Cab', 'Category': 'Pickup'},
        {'Year': 2008, 'Make': 'Mitsubishi', 'Model': 'Raider Extended Cab', 'Category': 'Pickup'},
        {'Year': 2018, 'Make': 'Ram', 'Model': '1500 Crew Cab', 'Category': 'Pickup'},
        {'Year': 2019, 'Make': 'Lincoln', 'Model': 'MKC', 'Category': 'SUV'},
        {'Year': 2001, 'Make': 'BMW', 'Model': '5 Series', 'Category': 'Wagon, Sedan'},
        {'Year': 2011, 'Make': 'Lincoln', 'Model': 'MKX', 'Category': 'SUV'},
        {'Year': 2001, 'Make': 'Buick', 'Model': 'LeSabre', 'Category': 'Sedan'},
        {'Year': 2019, 'Make': 'Toyota', 'Model': '86', 'Category': 'Coupe'},
        {'Year': 2019, 'Make': 'Kia', 'Model': 'Sorento', 'Category': 'SUV'}
    ]


def _lowerize(d: dict[str, Any]):
    return { k.lower(): v for k, v in d.items() }


def test_insert_detection(vehicles_manager: VehiclesManager):
    vehicles_manager.db.drop_db()
    vehicles_manager.db.generate_db()
    data = {'Year': 2007, 'Make': 'Ford', 'Model': 'F150 SuperCrew', 'Category': 'Pickup'}
    data.update({"id": uuid.uuid4(), "timestamp": 1})
    vid = vehicles_manager.add_detection(**_lowerize(data))
    assert vid is not None


def test_get_detections(vehicles_manager: VehiclesManager, vehicles: list[dict[str, Any]]):
    vehicles_manager.db.drop_db()
    vehicles_manager.db.generate_db()
    for v in vehicles:
        v.update({"id": uuid.uuid4(), "timestamp": 1})
        vehicles_manager.add_detection(**_lowerize(v))

    dects = vehicles_manager.detections()
    assert len(dects) == len(vehicles)
    for d in dects:
        assert type(d) == Detection


    sortedv = sorted(vehicles, key=lambda x: x["id"])
    for v1, v2 in zip(sortedv, dects):
        assert v1["id"] == v2.id


def test_skip_detections(vehicles_manager: VehiclesManager, vehicles: list[dict[str, Any]]):
    """
    Verifica que el skip funciona (por defecto el indice es el id)
    """
    vehicles_manager.db.drop_db()
    vehicles_manager.db.generate_db()
    to_insert = [_lowerize(v) for v in vehicles]
    for v in to_insert:
        v.update({"id": uuid.uuid4(), "timestamp": 1})
        vehicles_manager.add_detection(**v)

    sortedv = sorted(to_insert, key=lambda x: x["id"])
    vslice = sortedv[10:]

    dects = vehicles_manager.detections(skip=10)
    assert len(dects) == len(vslice)

    for v1, v2 in zip(dects, vslice):
        assert v1.id == v2["id"]


def test_vehicles_by_make(vehicles_manager: VehiclesManager, vehicles: list[dict[str, Any]]):
    """
        verifica que esté agregando correctamnete los vehículos.
    """
    makes = {m: 0 for m in (v["Make"] for v in vehicles)}
    for v in vehicles:
        makes[v["Make"]] += 1

    vehicles_manager.db.drop_db()
    vehicles_manager.db.generate_db()
    to_insert = [_lowerize(v) for v in vehicles]
    for v in to_insert:
        v.update({"id": uuid.uuid4(), "timestamp": 1})
        vehicles_manager.add_detection(**v)

    result = vehicles_manager.vehicles_by_make()
    print(result)

    for m in result:
        key = m.make
        assert makes[key] == m.count


def test_add_dup_detection(vehicles_manager: VehiclesManager):
    vehicles_manager.db.drop_db()
    vehicles_manager.db.generate_db()

    data = {'Year': 2007, 'Make': 'Ford', 'Model': 'F150 SuperCrew', 'Category': 'Pickup'}
    data.update({"id": uuid.uuid4(), "timestamp": 1})

    detection = Detection(**_lowerize(data))
    vehicles_manager.add_detection(**detection.dict())

    with pytest.raises(IntegrityError):
        vehicles_manager.add_detection(**detection.dict())

