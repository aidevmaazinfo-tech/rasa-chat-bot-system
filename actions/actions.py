import sqlite3
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


class ActionCheckSufficientFunds(Action):
    def name(self) -> Text:
        return "action_check_sufficient_funds"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        balance = 1000
        transfer_amount = tracker.get_slot("amount")

        has_sufficient_funds = transfer_amount <= balance

        return [SlotSet("has_sufficient_funds", has_sufficient_funds)]


class ActionCheckOrderStatus(Action):
    def name(self) -> Text:
        return "action_check_order_status"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        order_id = tracker.get_slot("order_id")

        if not order_id:
            dispatcher.utter_message(text="Please provide your order number.")
            return []

        try:
            connection = sqlite3.connect(r"C:\Hassan\task5\orders.db")
            cursor = connection.cursor()

            cursor.execute(
                "SELECT customer_name, status FROM orders WHERE order_id = ?",
                (str(order_id),),
            )

            order = cursor.fetchone()
            connection.close()

            if order:
                customer_name, status = order
                dispatcher.utter_message(
                    text=f"Order {order_id} for {customer_name} is currently {status}."
                )
            else:
                dispatcher.utter_message(
                    text=f"I couldn't find order {order_id} in our system."
                )

        except sqlite3.Error:
            dispatcher.utter_message(
                text="Sorry, I couldn't access the order database right now."
            )

        return []