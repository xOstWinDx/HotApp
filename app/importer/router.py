import csv
import datetime

from fastapi import APIRouter, UploadFile, File, HTTPException
from starlette import status

from app.bookings.dao import BookingsDAO
from app.hotels.dao import HotelsDAO
from app.hotels.rooms.dao import RoomsDAO

router = APIRouter(
    prefix='/import',
    tags=['Добавление данных из CSV']
)


@router.post("/hotels")
async def upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open(f'app/importer/{file.filename}', 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    with open(f'app/importer/{file.filename}', encoding='utf-8') as r_file:
        try:
            file_reader = csv.DictReader(r_file, delimiter=",")

            for row in file_reader:
                await HotelsDAO.add(
                    id=int(row['id']),
                    name=row['name'],
                    location=row['location'],
                    services=row['services'],
                    rooms_quantity=int(row['rooms_quantity']),
                    image_id=int(row['image_id'])
                )

                # await BookingsDAO.add(row['room_id'], datetime.datetime.strptime(row['date_from'], '%Y-%m-%d'),
                #                       datetime.datetime.strptime(row['date_to'], '%Y-%m-%d'), row['user_id'])
                #
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/rooms")
async def upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open(f'app/importer/{file.filename}', 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    with open(f'app/importer/{file.filename}', encoding='utf-8') as r_file:
        try:
            file_reader = csv.DictReader(r_file, delimiter=",")

            for row in file_reader:
                await RoomsDAO.add(
                    hotel_id=int(row['hotel_id']),
                    name=row['name'],
                    description=row['description'],
                    price=int(row['price']),
                    services=row['services'],
                    quantity=int(row['quantity']),
                    image_id=int(row['image_id'])
                )

                # await BookingsDAO.add(row['room_id'], datetime.datetime.strptime(row['date_from'], '%Y-%m-%d'),
                #                       datetime.datetime.strptime(row['date_to'], '%Y-%m-%d'), row['user_id'])
                #
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)



@router.post("/booking")
async def upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open(f'app/importer/{file.filename}', 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    with open(f'app/importer/{file.filename}', encoding='utf-8') as r_file:
        try:
            file_reader = csv.DictReader(r_file, delimiter=",")

            for row in file_reader:
                await BookingsDAO.add(
                    int(row['room_id']),
                    datetime.datetime.strptime(row['date_from'], '%Y-%m-%d'),
                    datetime.datetime.strptime(row['date_to'], '%Y-%m-%d'),
                    int(row['user_id']))

        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


