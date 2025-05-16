import json
import allure
from faker import Faker

from models.user import UserName


@allure.epic("[KAFKA][niffler-auth]: Паблишинг сообщений в кафку")
class TestAuthRegistrationKafkaTest:

    @allure.title("KAFKA: Сообщение с пользователем публикуется в Kafka после успешной регистрации")
    def test_message_should_be_produced_to_kafka_after_successful_registration(self, auth_client, kafka_client,
                                                                               fake_user):
        username = fake_user.username
        password = fake_user.password

        topic_partitions = kafka_client.subscribe_listen_new_offsets("users")

        result = auth_client.register(username, password)
        assert result.status_code == 201

        event = kafka_client.log_msg_and_json(topic_partitions)

        with allure.step("Check that message from kafka exist"):
            assert event != '' and event != b''

        with allure.step("Check message content"):
            UserName.model_validate(json.loads(event.decode('utf8')))
            assert json.loads(event.decode('utf8'))['username'] == username

    @allure.title("KAFKA: Заполнение userdata исключая aut")
    def test_message_should_be_produced_to_userdata_after_kafka_event(self, kafka_client, auth_db, userdata_db,
                                                                      register_credential):
        username = register_credential.username

        kafka_client.produce_event("users", username)

        with allure.step("Check the record did not appear in the auth db"):
            username_auth_db = auth_db.get_user_by_username(username)
            assert username_auth_db is None, f"username {username} in database"

        with allure.step("Username in userdata db"):
            username_userdata_db = userdata_db.get_user(username).username
            assert username_userdata_db == username
