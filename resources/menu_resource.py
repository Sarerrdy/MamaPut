import logging

from flask import request
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from database import db
from models.menu import Menu
from schemas.menu_schema import MenuSchema

MENUS_ENDPOINT = "/api/menus"
logger = logging.getLogger(__name__)


class MenusResource(Resource):
    def get(self, id=None):
        """
        MenusResource GET method. Retrieves all menus found in the mamaput
        database, unless the id path parameter is provided. If this id
        is provided then the menu with the associated id is retrieved.

        :param id: Menu ID to retrieve, this path parameter is optional
        :return: Menu, 200 HTTP status code
        """
        if not id:
            status = request.args.get("status")
            logger.info(
                f"Retrieving all addresses, optionally filtered by "
                f"status={status}"
            )

            return self._get_all_menus(status), 200

        logger.info(f"Retrieving menus by id {id}")

        try:
            return self._get_menu_by_id(id), 200
        except NoResultFound:
            abort(404, message="menu not found")

    # get endpoint for single items

    def _get_menu_by_id(self, menu_id):
        """retrieve menu by menu id"""
        menu = Menu.query.filter_by(menu_id=menu_id).first()
        menu_json = MenuSchema().dump(menu)

        if not menu_json:
            raise NoResultFound()

        logger.info(f"Menu retrieved from database {menu_json}")
        return menu_json

    # get endpoint for all items

    def _get_all_menus(self, status):
        """retrieve all menus"""
        if status:
            menus = Menu.query.filter_by(status=status).all()
        else:
            menus = Menu.query.all()

        menus_json = [
            MenuSchema().dump(menu) for menu in menus]

        logger.info("Menu successfully retrieved.")
        return menus_json

    # post endpoint

    def post(self):
        """
        MenusResource POST method. Adds a new menu item to the database.

        :return: menu.menu_id, 201 HTTP status code.
        """
        menu = MenuSchema().load(request.get_json())

        try:
            db.session.add(menu)
            db.session.commit()
        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this menu is already in the database. "
                f"Error: {e}"
            )

            abort(500, message="Unexpected Error!")
        else:
            return menu.menu_id, 201

    # delete endpoint

    def delete(self, menu_id):
        """
        MenusResource DELETE method. Deletes a menu item from the database.

        :param menu_id: ID of the menu item to delete.
        :return: 200 HTTP status code if successful, 404 if not found.
        """
        menu = Menu.query.filter_by(menu_id=menu_id).first()
        if menu is None:
            abort(404, message="Menu item not found!")

        try:
            db.session.delete(menu)
            db.session.commit()
        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, could not delete menu item. "
                f"Error: {e}"
            )
            abort(500, message="Unexpected Error!")
        else:
            logger.info({'Menu item deleted successfully'})
            return menu.menu_id, 200

    # Put endpoint

    def put(self, menu_id):
        """
        MenusResource PUT method. Updates a menu item in the database.

        :param menu_id: ID of the menu item to update.
        :return: Updated menu item JSON, 200 HTTP status code if successful,
        404 if not found.
        """
        menu = Menu.query.filter_by(menu_id=menu_id).first()
        if menu is None:
            abort(404, message="Menu item not found!")

        try:
            menu_data = request.get_json()
            menu = MenuSchema().load(menu_data, instance=menu, partial=True)
            db.session.commit()
        # except ValidationError as err:
        #     abort(400, message=err.messages)
        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, could not update menu item. "
                f"Error: {e}"
            )
            abort(500, message="Unexpected Error!")
        else:
            return (MenuSchema().dump(menu)), 200
