from app.marketmind.knowledge.angles import ANGLES
class CopyAgent:
    def run(self, property_data: dict, style: str) -> dict:
        style = style if style in ANGLES else "auto"
        angles = ANGLES[style]
        return {"style": style, "primary_angle": angles[0], "secondary_angles": angles[1:], "positioning": f"{property_data['type']} con foco en {angles[0]}", "agent": "CopyAgent"}
