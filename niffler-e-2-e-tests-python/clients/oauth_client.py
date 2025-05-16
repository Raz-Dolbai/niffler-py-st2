import pkce
from models.config import Envs
from models.oauth_model import OAuthRequest
from utils.sessions import AuthSession


class OAuthClient:
    """Авторизует по OAUTH 2.0"""
    session: AuthSession
    base_url: str

    def __init__(self, envs: Envs):
        """Генерируем code_verifier, code_challenge, basic_auth_token из секрета сервиса авторизации"""
        self.session = AuthSession(base_url=envs.auth_url)
        self.code_verifier, self.code_challenge = pkce.generate_pkce_pair()
        self.redirect_uri = envs.frontend_url + "/authorized"
        # Этот код мы написали самостоятельно и заменили на использование библиотеки
        # self.code_verifier = base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8')
        # self.code_verifier = re.sub('[^a-zA-Z0-9]+', '', self.code_verifier)
        # self.code_challenge = hashlib.sha256(self.code_verifier.encode('utf-8')).digest()
        # self.code_challenge = base64.urlsafe_b64encode(self.code_challenge).decode('utf-8')
        # self.code_challenge = self.code_challenge.replace('=', '')

    def get_token(self, username, password):
        """Возвращаем auth token для авторизации пользователя
            1. Получаем jsession и xsrf token куку в сессию
            2. Получаем code из redirect по xsrf token
            3. Получаем id_token"""
        xsrf_response = self.session.get(
            url="/oauth2/authorize",
            params=OAuthRequest(redirect_uri=self.redirect_uri,
                                code_challenge=self.code_challenge).model_dump(),
            allow_redirects=True)
        xsrf_response.raise_for_status()

        code_response = self.session.post(
            url="/login",
            data={
                "_csrf": self.session.cookies.get("XSRF-TOKEN"),
                "username": username,
                "password": password}, allow_redirects=True)
        code_response.raise_for_status()

        token_response = self.session.post(
            url="/oauth2/token",
            data={
                "code": self.session.code,
                "redirect_uri": self.redirect_uri,
                "code_verifier": self.code_verifier,
                "grant_type": "authorization_code",
                "client_id": "client"
            }
        )
        token_response.raise_for_status()
        self.token = token_response.json().get("id_token", None)
        return self.token

    def register(self, username: str, password: str):
        self.session.get(
            url="/register",
            params={
                "redirect_uri": "http://auth.niffler.dc:9000/register",
            },
            allow_redirects=True
        )

        result = self.session.post(
            url="/register",
            data={
                "username": username,
                "password": password,
                "passwordSubmit": password,
                "_csrf": self.session.cookies.get("XSRF-TOKEN")
            },
            allow_redirects=True
        )
        return result