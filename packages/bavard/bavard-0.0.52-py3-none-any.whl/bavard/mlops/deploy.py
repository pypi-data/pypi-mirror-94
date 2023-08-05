from fire import Fire
import uvicorn
from bavard_ml_common.mlops.pub_sub import PubSub

from bavard.mlops.pipeline import ChatbotPipeline
from bavard import config


def deploy(
    *,
    project_id: str,
    agent_uname: str,
    publish_id: str,
    model_name: str,
    model_version: str,
    model_dir: str,
    **uvicorn_settings,
) -> None:
    """
    Loads a `ChatbotPipeline` instance from `model_dir` (a directory), converts it into
    a web service, then runs the web service using the args in `uvicorn_settings`.
    """
    # Load the model and convert to web service.
    model = ChatbotPipeline.from_dir(model_dir)
    app = model.to_app()

    # Notify the model is ready and start the app.
    if not config.IS_TEST:
        PubSub(project_id).notify_model_ready(
            agent_uname, publish_id, model_name, model_version
        )
    uvicorn.run(app, **uvicorn_settings)


if __name__ == "__main__":
    Fire(deploy)
