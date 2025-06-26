from tools.cancel_tool import CancelOrderTool
from tools.track_tool import TrackOrderTool
from tools.return_tool import ReturnOrderTool
from tools.refund_tool import RefundStatusTool
from tools.reset_tool import PasswordResetTool

tool_registry = {
    "CancelOrder": CancelOrderTool,
    "TrackOrder": TrackOrderTool,
    "ReturnOrder": ReturnOrderTool,
    "RefundStatus": RefundStatusTool,
    "PasswordReset": PasswordResetTool
}
