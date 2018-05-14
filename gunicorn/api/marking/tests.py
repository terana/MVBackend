import pytest
from channels.testing import WebsocketCommunicator
from django.contrib.auth.models import User

from .consumers import MarkingConsumer
from ..models import Event


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
class TestMarking(object):
    @classmethod
    @pytest.fixture(autouse=True)
    def setup_class(cls):
        user = User(username='testuser')
        user.set_password('12345')
        user.save()
        cls.user = user

        event = Event(creator=user)
        event.save()
        event.users.set([user])
        event.save()
        cls.event = event

    async def test_connection(self):
        communicator = WebsocketCommunicator(MarkingConsumer, "ws/marking?event_id={eid}".format(eid=self.event.uuid))
        communicator.scope['user'] = self.user
        connected, _ = await communicator.connect()
        assert connected

        response = await communicator.receive_json_from()
        assert response.get('marking_list') is not None
        await communicator.disconnect()

    async def test_connection_non_existing_event(self):
        communicator = WebsocketCommunicator(MarkingConsumer, "ws/marking?event_id={eid}".format(eid='non-existing'))
        communicator.scope['user'] = self.user
        connected, _ = await communicator.connect()
        assert connected

        response = await communicator.receive_output()
        assert response['type'] == 'websocket.close'
        await communicator.disconnect()

    async def test_connection_no_event(self):
        communicator = WebsocketCommunicator(MarkingConsumer, "ws/marking")
        communicator.scope['user'] = self.user
        connected, _ = await communicator.connect()
        assert connected

        response = await communicator.receive_output()
        assert response['type'] == 'websocket.close'
        await communicator.disconnect()

    async def test_prepare_to_mark(self):
        communicator = WebsocketCommunicator(MarkingConsumer, "ws/marking?event_id={eid}".format(eid=self.event.uuid))
        communicator.scope['user'] = self.user
        connected, _ = await communicator.connect()
        assert connected
        await communicator.send_json_to({"message": "prepare_to_mark", 'params': {'user_id': 1234}})
        response = await communicator.receive_json_from()
        assert response == {'result': 'ok'}
        await communicator.disconnect()
