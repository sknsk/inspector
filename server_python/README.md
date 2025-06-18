# MCP Inspector Python Server

이 디렉터리는 Node.js 기반 `server` 디렉터리의 기능을 파이썬 3.13.1 환경에서 동작하도록 포팅한 예시입니다.
FastAPI 기반으로 동작하며 `mcp[cli]` 패키지의 Model Context Protocol SDK를 사용합니다.

`/mcp` 엔드포인트는 Streamable HTTP 프로토콜을 사용해 브라우저와 MCP 서버 간의 스트림 통신을 중계합니다.

## 요구 사항

- Python 3.13.1 (테스트 환경에서는 3.12.x 사용)
- `pip install -r requirements.txt`

## 실행 방법

```bash
uvicorn server_python.app:app --host 127.0.0.1 --port 6277
```
