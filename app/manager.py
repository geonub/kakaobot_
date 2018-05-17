from app import db
from .message import BaseMessage, HomeMessage, SuccessMessage, FailMessage
from .model import User, Session
from .contents import Contents
from .keyboard import Keyboard

class Singleton(type):
    instance = None

    def __call__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance


class APIManager(metaclass=Singleton):
    def process(self, mode, *args):
        try:
            options = {
                "home": self.return_home_keyboard,
                "message": self.handle_message,
                "add": self.add_friend,
                "block": self.block_friend,
                "exit": self.exit_chatroom,
            }
            message = options.get(mode)(*args)
            response_code = 200
        except:
            message = self.handle_fail()
            response_code = 400
        finally:
            return message, response_code

    def return_home_keyboard(self):
        """
        [GET] your_server_url/keyboard 일 때 사용되는 함수입니다.
        """
        message = MessageHandler.get_home_message()
        return message

    def handle_message(self, data):
        """
        [POST] your_server_url/message 일 때 사용되며
        사용자가 전달한 data에 따라 처리 과정을 거쳐 메시지를 반환하는 메인 함수입니다.
        """
        user_key = data["user_key"]
        request_type = data["type"]
        content = data["content"]

        if content == "금융 정보":
            message = MessageHandler.get_mi_message()
            return message

        if content == "순위 보여줘":
            message = MessageHandler.get_rank_message()
            return message

        if content == "맞춤법 알려줘":
            message = MessageHandler.get_typing_message(1)
            return message

        if content == "취소":
            message = MessageHandler.get_cancel_message()
            DBHandler.delete_user(user_key)
            return message

        if content == "나가기":
            message = MessageHandler.get_cancel_message()
            DBHandler.delete_user(user_key)
            return message

        """step1"""
        index_table = ["증시", "현물", "환율"]
        if content in index_table:
            message = MessageHandler.get_index_message(index_table.index(content))
            return message

        if content == "종목 검색":
            DBHandler.add_user(user_key,'Y')
            message = MessageHandler.get_typing_message(0)
            return message

        if DBHandler.query(Session, user_key=user_key, stock='Y'):
            message = MessageHandler.get_stock_message(content)
            return message
        else:
            message = MessageHandler.get_spell_message(content)
            return message


    def add_friend(self, data):
        """
        [POST] your_server_url/friend 일 때 사용되는 함수입니다.
        기본 동작으로 수집된 user_key를 DB에 추가합니다.
        """
        user_key = data["user_key"]
        DBHandler.add_user(user_key)
        message = MessageHandler.get_success_message()
        return message

    def block_friend(self, user_key):
        """
        [DELETE] your_server_url/friend/{user_key} 일 때 사용되는 함수입니다.
        기본 동작으로 수집된 user_key를 DB에서 제거합니다.
        """
        DBHandler.delete_user(user_key)
        message = MessageHandler.get_success_message()
        return message

    def exit_chatroom(self, user_key):
        """
        [DELETE] your_server_url/chat_room/{user_key} 일 때 사용되는 함수입니다.
        """
        message = MessageHandler.get_success_message()
        return message

    def handle_fail(self):
        """
        처리 중 예외가 발생했을 때 사용되는 함수입니다.
        """
        message = MessageHandler.get_fail_message()
        return message


class MessageManager(metaclass=Singleton):

    def get_base_message(self):
        base_message = BaseMessage().get_message()
        return base_message

    def get_home_message(self):
        home_message = HomeMessage().get_message()
        return home_message

    def get_mi_message(self):
        mi_message = BaseMessage()
        mi_message.update_message("어떤 지표요?")
        mi_message.update_keyboard(Keyboard().index_buttons)
        mi_message = mi_message.get_message()
        return mi_message

    def get_index_message(self,indexing):
        index_message = BaseMessage()
        if indexing == 0:
            contents = Contents().get_stock_contents()
        elif indexing == 1:
            contents = Contents().get_goods_contents()
        elif indexing == 2:
            contents = Contents().get_exchange_contents()

        index_message.update_message(contents)
        index_message = index_message.get_message()
        return index_message

    def get_cancel_message(self):
        cancel_message = BaseMessage()
        cancel_message.update_message("초기화면으로 돌아갑니다.")
        cancel_message = cancel_message.get_message()
        return cancel_message

    def get_typing_message(self,index):
        typing_message = BaseMessage()
        contents = Contents().get_typing_mode_contents(index)
        typing_message.update_message(contents)
        typing_message.remove_keyboard()
        typing_message = typing_message.get_message()
        return typing_message

    def get_stock_message(self,content):
        stock_message = BaseMessage()
        try:
            contents = Contents().get_want_stock_contents(content)
        except:
            contents = "검색 결과가 없습니다."
        stock_message.update_message(contents)
        stock_message.remove_keyboard()
        stock_message = stock_message.get_message()
        return stock_message

    def get_spell_message(self,content):
        spell_message = BaseMessage()
        try:
            contents = Contents().get_spell_contents(content)
        except:
            contents = "맞춤법 검사 결과를 불러오지 못했습니다."
        spell_message.update_message(contents)
        spell_message.remove_keyboard()
        spell_message = spell_message.get_message()
        return spell_message

    def get_fail_message(self):
        fail_message = FailMessage().get_message()
        return fail_message

    def get_success_message(self):
        success_message = SuccessMessage().get_message()
        return success_message

    def get_rank_message(self):
        rank_message = BaseMessage()
        contents = Contents().get_rank_contents()
        rank_message.update_message(contents)
        rank_message = rank_message.get_message()
        return rank_message

class DBManager(metaclass=Singleton):
    def query(self, model, **kwargs):
        return model.query.filter_by(**kwargs).first()

    def delete(self, obj):
        db.session.delete(obj)
        self.commit()

    def delete_user(self, user_key):
        user = self.query(Session, user_key=user_key)
        if user:
            self.delete(user)

    def add(self, obj):
        db.session.add(obj)
        self.commit()

    def add_user(self, user_key, stock):
        user = self.query(Session, user_key=user_key)
        if not user:
            user = Session(user_key, stock)
            self.add(user)

    def commit(self):
        db.session.commit()

APIHandler = APIManager()
MessageHandler = MessageManager()
DBHandler = DBManager()
