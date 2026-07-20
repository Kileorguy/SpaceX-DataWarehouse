import json
import traceback
from database import SessionLocal
from models import SpacecraftDimension

def load_dimension(
    model,
    json_file,
    unique_key,
    transform
):

    db = SessionLocal()

    try:

        with open(json_file, encoding="utf-8") as f:

            raw_data = json.load(f)
        if isinstance(raw_data, dict):
            raw_data = raw_data["results"]

        existing = {

            row[0]

            for row in db.query(
                getattr(model, unique_key)
            ).all()
        }

        objects = []

        for row in raw_data:

            transformed_rows = transform(row)

            if transformed_rows is None:
                continue

            if not isinstance(transformed_rows, list):
                transformed_rows = [transformed_rows]

            for clean_row in transformed_rows:

                if clean_row is None:
                    continue

                key = clean_row[unique_key]

                if model == SpacecraftDimension:

                    existing_row = db.query(
                        SpacecraftDimension
                    ).filter(
                        SpacecraftDimension.spacecraft_id == key
                    ).first()

                    if existing_row:

                        for column, value in clean_row.items():

                            setattr(
                                existing_row,
                                column,
                                value
                            )

                        continue

                if key in existing:
                    continue

                objects.append(
                    model(**clean_row)
                )

                existing.add(key)

        db.bulk_save_objects(objects)

        db.commit()

        print(
            f"{model.__tablename__}: "
            f"{len(objects)} inserted"
        )

    except Exception as e:

        db.rollback()
        print("error")

        print(e)
        traceback.print_exc()

    finally:

        db.close()


def load_fact(
    model,
    json_file,
    unique_key,
    transform,
    lookups
):

    db = SessionLocal()

    try:

        with open(json_file, encoding="utf-8") as f:

            raw_data = json.load(f)

        if isinstance(raw_data, dict):
            raw_data = raw_data["results"]

        existing = {

            row[0]

            for row in db.query(
                getattr(model, unique_key)
            ).all()
        }

        objects = []

        for row in raw_data:

            transformed_rows = transform(
                row,
                lookups
            )

            if transformed_rows is None:
                continue

            if not isinstance(
                transformed_rows,
                list
            ):
                transformed_rows = [
                    transformed_rows
                ]

            for clean_row in transformed_rows:

                if clean_row is None:
                    continue

                key = clean_row[unique_key]

                if key in existing:
                    continue

                objects.append(
                    model(**clean_row)
                )

                existing.add(key)

        if objects:

            db.bulk_save_objects(
                objects
            )

            db.commit()

        print(
            f"{model.__tablename__}: "
            f"{len(objects)} inserted"
        )

    except Exception as e:

        db.rollback()

        print(e)

        traceback.print_exc()

    finally:

        db.close()