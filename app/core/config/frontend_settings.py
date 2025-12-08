from pydantic_settings import BaseSettings, SettingsConfigDict


class FrontendSettings(BaseSettings):
    image_size_avatar_small: str = "100,100,center"
    image_size_avatar_medium: str = "200,200,center"
    image_size_avatar_large: str = "640,640,center"

    image_size_location_small: str = "200,200,center"
    image_size_location_medium: str = "640,640 center"
    image_size_location_large: str = "1024,1024,center"

    image_size_event_small: str = "200,200,center"
    image_size_event_medium: str = "640,640 center"
    image_size_event_large: str = "1024,1024,center"

    image_size_tag_icon_small: str = "50,50,center"
    image_size_tag_icon_medium: str = "100,100 center"

    model_config = SettingsConfigDict(
        env_prefix="FRONTEND_",
        extra="ignore"
    )
