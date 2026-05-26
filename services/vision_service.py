from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

from config import AZURE_VISION_ENDPOINT, AZURE_VISION_KEY


def analyze_image(image_bytes):
    client = ImageAnalysisClient(
        endpoint=AZURE_VISION_ENDPOINT,
        credential=AzureKeyCredential(AZURE_VISION_KEY)
    )

    result = client.analyze(
        image_data=image_bytes,
        visual_features=[
            VisualFeatures.CAPTION,
            VisualFeatures.TAGS,
            VisualFeatures.OBJECTS
        ]
    )

    caption = ""
    tags = []
    objects = []

    if result.caption is not None:
        caption = result.caption.text

    if result.tags is not None:
        tags = [tag.name for tag in result.tags.list]

    if result.objects is not None:
        objects = [obj.tags[0].name for obj in result.objects.list if obj.tags]

    return {
        "caption": caption,
        "tags": tags,
        "objects": objects
    }