import json

from allure import step, epic, suite, title, id, tag
from faker import Faker

from models.user import UserName


@epic("[KAFKA][niffler-auth]: Паблишинг сообщений в кафку")
@suite("[KAFKA][niffler-auth]: Паблишинг сообщений в кафку")
class TestAuthRegistrationKafkaTest:
    @id("600001")
    @title("KAFKA: Сообщение с пользователем публикуется в Kafka после успешной регистрации")
    @tag("KAFKA")
    def test_message_should_be_produced_to_kafka_after_successful_registration(self, auth_client, kafka_client):
        username = Faker().user_name()
        password = Faker().password(special_chars=False)
        print(kafka_client.list_topics_names())

        # topic_partitions = kafka_client.subscribe_listen_new_offsets("users")
        #
        # result = auth_client.register(username, password)
        # assert result.status_code == 201
        #
        # event = kafka_client.log_msg_and_json(topic_partitions)
        #
        # with step("Check that message from kafka exist"):
        #     assert event != '' and event != b''
        #
        # with step("Check message content"):
        #     UserName.model_validate(json.loads(event.decode('utf8')))
        #     assert json.loads(event.decode('utf8'))['username'] == username
