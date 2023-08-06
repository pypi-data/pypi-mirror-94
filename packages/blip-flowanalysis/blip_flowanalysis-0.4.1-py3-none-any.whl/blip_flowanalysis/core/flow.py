from __future__ import nested_scopes
import typing as tp
import json

from blip_flowanalysis.errors import FlowParameterError, FlowTypeError

Track_report = tp.Dict[str, tp.List[tp.Dict[str, str]]]


class Flow(object):
    """Represents chatbot flow structure.
    
    This class provide useful information about the chatbot using it's configuration json.
    You'll need this class to make analysis using this package analysis classes.
    
    Where find the flow structure:
    The json this class uses come from `OwnerCallerValue` table that can be found following these steps:
    1. portal.blip.ai (login needed)
    2. your_chatbot
    3. configurations
    4. basic configurations
    5. advanced configurations
    6. On table with Owner, Caller, choose the 'Value' column
    
    Attributes:
        * identity (str) - chatbot identifier
        * structure (dict) - flow structure
        * chatbot_type (str) - can be "router", "service", "standalone" or "unknown"
        * receive_router_context (bool) - True or False if receives context, None if not "service"
    
    Methods:
        * get_states_list - Return the flow state list if chatbot is not `router`; otherwise raise FlowTypeError
        * get_children_list - Return children list if chatbot is `router`; otherwise raise FlowTypeError
        * get_tracks_id - Return track identification information
    """
    
    def __init__(self, json_obj: str) -> None:
        super().__init__()
        self.__create_class_attributes(json_obj)
    
    def __create_class_attributes(self, json_obj: str) -> None:
        """Encapsulate the class attribute initializations that depends on self.__structure"""
        self.__structure = json.loads(json_obj)
        self.identity = self.__structure.get("identifier", "null")
        self.chatbot_type = self.__get_chatbot_type()
        self.receive_router_context = self.__get_receive_router_context()
        
        self.__validate_flow_settings()
    
    @property
    def structure(self):
        return self.__structure
    
    @structure.setter
    def structure(self, json_obj: str):
        self.__create_class_attributes(json_obj)
    
    def __str__(self):
        """Return str(self.__structure)."""
        return str(self.__structure)
    
    def __len__(self):
        """Return len(self.__structure)."""
        return len(self.__structure)
    
    def __validate_flow_settings(self) -> None:
        """Validate if structure has settings."""
        if "settings" not in self.__structure:
            raise FlowParameterError("JSON must have 'settings' key.")
    
    def __validate_flow_states(self) -> None:
        """Validate if structure has flow and states."""
        if "flow" not in self.__structure["settings"]:
            raise FlowParameterError("JSON must have 'flow' key inside 'settings' structure.")
        if "states" not in self.__structure["settings"]["flow"]:
            raise FlowParameterError("JSON must have 'states' key inside 'flow' structure.")
    
    def __is_router(self) -> bool:
        """The chatbot can have "children" or "flow" in the "settings" key:
            * "children" only appears for router
            * "flow" for all other types
        """
        answer = self.__structure["settings"].keys()
        return True if "children" in answer else False
    
    def __is_service(self) -> bool:
        if self.__is_router():
            return False
        
        try:
            context = self.__structure["settings"]["flow"]["configuration"].keys()
            return True if "builder:useTunnelOwnerContext" in context else False
        except KeyError as e:
            raise FlowParameterError("Missing key", str(e), "on structure")
    
    def __get_chatbot_type(self) -> str:
        """True table for __get_chatbot_type:
        | is_router | is_service | interpretation |
        |-----------|-----------------|----------------|
        | False     | False           | standalone     |
        | False     | True            | service        |
        | True      | False           | router         |
        | True      | True            | unknown        |
        """
        router = self.__is_router()
        service = self.__is_service()
        
        if not router and not service:
            # False and False -> standalone
            return "standalone"
        
        elif not router and service:
            # False and True
            return "service"
        
        elif router and not service:
            # True and False
            return "router"
            
        else:
            # True and True
            return "unknown"
    
    def __get_receive_router_context(self) -> str:
        if self.__is_service():
            try:
                return self.__structure["settings"]["flow"]["configuration"]["builder:useTunnelOwnerContext"]
            except KeyError as e:
                raise FlowParameterError("Missing key", str(e), "on structure")
        else:
            return ""
    
    def get_states_list(self) -> list:
        """Return the flow state list if chatbot is not `router`."""
        self.__validate_flow_states()
        if self.__is_router():
            raise FlowTypeError("Router doesn't have flow states.")
    
        try:
            return self.__structure["settings"]["flow"]["states"]
        except KeyError as e:
            FlowParameterError("Missing key", str(e), "on structure")
    
    def get_tracks_id(self) -> Track_report:
        """Return track identification information.

         Tracking is recommended for analytics reports in Blip portal - (source)[https://docs.blip.ai/#analytics].
         The identification information are: `state-id`, `input_type` and `action`

         :return: For every `track_name` a list of info for id.
         :rtype: ``tp.Dict[str, tp.List[tp.Dict[str, str]]]``
         """
    
        def __insert_action(type: str, id: str) -> None:
            """Internal method to filter track info"""
            if action["type"] == "TrackEvent":
                key = action["settings"]["category"]
            
                track_filter = {
                    "state-id": id,
                    "input_type": type,
                    "action": action["settings"].get("action")
                }
                if tracking_dict.get(key):
                    tracking_dict[key].append(track_filter)
                else:
                    tracking_dict[key] = [track_filter]
    
        state_list = self.get_states_list()
        tracking_dict = dict()
        for state in state_list:
            for action in state["inputActions"]:
                __insert_action(type="inputActions", id=state["id"])
        
            for action in state["outputActions"]:
                __insert_action(type="outputActions", id=state["id"])
    
        return tracking_dict
    
    def get_children_list(self) -> tp.List[tp.Dict[str, str]]:
        """Return children list if chatbot is `router`.
        
        :raise FlowTypeError: if chatbot_type is not 'router'.
        :raise FlowParameterError: if some key is missing from structure.
        
        :return: Children list with parameters
        :rtype: ``typing.List[tp.Dict[str, str]]``
        """
        if self.__is_router():
            try:
                return self.structure["settings"]["children"]
            except KeyError as e:
                raise FlowParameterError("Missing key", str(e), "on structure")
        else:
            raise FlowTypeError("Only `router` has children list.")
