import http from "k6/http";
import { check } from "k6";

export const options = {
    stages: [
        { duration: "10s", target: 10 },
        { duration: "20s", target: 20 },
        { duration: "30s", target: 35 },
        { duration: "35s", target: 50 },
        { duration: "15s", target: 25 },
        { duration: "10s", target: 0  },
    ], 

    thresholds: {
        http_req_duration: [
            "p(95)<200",
            "p(99)<500",
        ],
        http_req_failed: ["rate<0.01"],
    }
}

const PAGE_ID = "1129462363577012"

export default function () {
    const payload = JSON.stringify({
        object: "page",
        entry: [{
            id: PAGE_ID,
            time: Date.now(),
            messaging: [{
                sender:    { id: `USER_${__VU}_${__ITER}` },
                recipient: { id: PAGE_ID },
                timestamp: Date.now(),
                message: {
                    mid:  `mid_${__VU}_${__ITER}_${Date.now()}`,
                    text: "Hello benchmark!"
                }
            }]
        }]
    })

    const res = http.post(
        "http://localhost:8000/channel-accounts/webhooks/facebook",
        payload,
        { headers: { "Content-Type": "application/json" } }
    )

    check(res, {
        "status 200":  (r) => r.status === 200,
        "has task_id": (r) => JSON.parse(r.body).task_id !== undefined,
    })
}