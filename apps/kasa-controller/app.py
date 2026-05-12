import asyncio
import os
import ipaddress
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import yaml
from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    Header,
    Request,
    APIRouter,
)
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from kasa import Discover
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

CONFIG_PATH = "/config/devices.yaml"

API_TOKEN = os.getenv("KS300_API_TOKEN", "").strip()
ALLOWLIST_RAW = os.getenv("KS300_ALLOWLIST", "").strip()

UI_HTML = r"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>KS300 Local Control</title>
    <style>
    :root {
        --bg: #0f1115;
        --panel: #171a21;
        --panel-2: #1e222c;
        --border: #2a2f3a;
        --text: #e6e9ef;
        --muted: #9aa4b2;
        --accent: #4ea1ff;
        --green: #3ddc97;
        --red: #ff6b6b;
        --button-bg: #222735;
        --button-hover: #2d3345;
        --input-bg: #121622;
    }

    * {
        box-sizing: border-box;
    }

    body {
        font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
        margin: 18px;
        background: var(--bg);
        color: var(--text);
    }

    .row {
        display: flex;
        gap: 12px;
        align-items: center;
        flex-wrap: wrap;
    }

    .top {
        justify-content: space-between;
        margin-bottom: 14px;
    }

    .card {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 14px;
        margin: 12px 0;
    }

    .strip-title {
        font-weight: 700;
        font-size: 16px;
        margin-bottom: 10px;
    }

    .outlets {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
    }

    .outlet {
        background: var(--panel-2);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 12px;
        min-width: 220px;
    }

    .name {
        font-weight: 600;
        margin-bottom: 6px;
    }

    .meta {
        color: var(--muted);
        font-size: 12px;
        margin-bottom: 10px;
    }

    button {
        padding: 8px 12px;
        border-radius: 10px;
        border: 1px solid var(--border);
        background: var(--button-bg);
        color: var(--text);
        cursor: pointer;
        transition: background 0.15s ease, border-color 0.15s ease;
    }

    button:hover {
        background: var(--button-hover);
        border-color: var(--accent);
    }

    button:active {
        transform: translateY(1px);
    }

    .on {
        color: var(--green);
        font-weight: 700;
    }

    .off {
        color: var(--red);
        font-weight: 700;
    }

    .muted {
        color: var(--muted);
        font-size: 12px;
    }

    input[type="password"],
    input[type="text"] {
        padding: 8px 10px;
        border-radius: 10px;
        border: 1px solid var(--border);
        background: var(--input-bg);
        color: var(--text);
        min-width: 280px;
    }

    input::placeholder {
        color: #6f7785;
    }

    code {
        background: #10131a;
        padding: 2px 6px;
        border-radius: 6px;
        border: 1px solid var(--border);
        color: var(--accent);
    }

    .err {
        color: var(--red);
        white-space: pre-wrap;
        margin-bottom: 10px;
    }

    a {
        color: var(--accent);
        text-decoration: none;
    }

    a:hover {
        text-decoration: underline;
    }
    </style>

</head>
<body>
  <div class="row top">
    <div>
      <div style="font-weight:800; font-size:18px;">KS300 Local Control</div>
      <div class="muted">Uses <code>/v1/strips</code> and <code>/toggle</code>. Auto-refreshes.</div>
    </div>
    <div class="row">
      <label class="muted" for="token">Bearer token:</label>
      <input id="token" type="password" placeholder="(optional) paste KS300_API_TOKEN" />
      <button onclick="saveToken()">Save</button>
      <button onclick="clearToken()">Clear</button>
    </div>
  </div>

  <div class="row" style="margin-bottom:10px;">
    <button onclick="refresh()">Refresh now</button>
    <span id="status" class="muted"></span>
  </div>

  <div id="error" class="err"></div>
  <div id="app"></div>

<script>
  const tokenEl = document.getElementById("token");
  const statusEl = document.getElementById("status");
  const errEl = document.getElementById("error");
  const appEl = document.getElementById("app");

  function loadToken() {
    const t = localStorage.getItem("ks300_token") || "";
    tokenEl.value = t;
    return t;
  }
  function saveToken() {
    localStorage.setItem("ks300_token", tokenEl.value.trim());
    refresh();
  }
  function clearToken() {
    localStorage.removeItem("ks300_token");
    tokenEl.value = "";
    refresh();
  }

  function authHeaders() {
    const t = tokenEl.value.trim();
    return t ? { "Authorization": "Bearer " + t } : {};
  }

  async function apiGet(path) {
    const res = await fetch(path, { headers: { ...authHeaders() } });
    if (!res.ok) {
      const text = await res.text();
      throw new Error(`GET ${path} -> ${res.status}\n${text}`);
    }
    return await res.json();
  }

  async function apiPost(path) {
    const res = await fetch(path, { method: "POST", headers: { ...authHeaders() } });
    if (!res.ok) {
      const text = await res.text();
      throw new Error(`POST ${path} -> ${res.status}\n${text}`);
    }
    return await res.json();
  }

  function fmtWatts(w) {
    if (w === null || w === undefined || Number.isNaN(w)) return "—";
    // show 1 decimal under 100W, else integer
    return (w < 100 ? w.toFixed(1) : Math.round(w).toString()) + " W";
  }

  function outletCard(stripId, outlet) {
    const stateClass = outlet.is_on ? "on" : "off";
    const stateText = outlet.is_on ? "ON" : "OFF";
    const watts = fmtWatts(outlet.power_w);

    return `
      <div class="outlet">
        <div class="name">${escapeHtml(outlet.name || ("Outlet " + outlet.index))}</div>
        <div class="meta">
          State: <span class="${stateClass}">${stateText}</span>
          &nbsp; • &nbsp;
          Power: <span>${watts}</span>
        </div>
        <div class="row">
          <button onclick="toggleOutlet('${stripId}', ${outlet.index})">Toggle</button>
          <button onclick="setOutlet('${stripId}', ${outlet.index}, 'on')">On</button>
          <button onclick="setOutlet('${stripId}', ${outlet.index}, 'off')">Off</button>
        </div>
      </div>
    `;
  }

  function stripCard(strip) {
    const outlets = (strip.outlets || []).map(o => outletCard(strip.id, o)).join("");
    return `
      <div class="card">
        <div class="strip-title">${escapeHtml(strip.name)} <span class="muted">(${strip.host})</span></div>
        <div class="row" style="margin-bottom:10px;">
          <button onclick="allOff('${strip.id}')">All Off</button>
        </div>
        <div class="outlets">${outlets}</div>
      </div>
    `;
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
  }

  async function refresh() {
    errEl.textContent = "";
    statusEl.textContent = "Loading…";
    try {
      const data = await apiGet("/v1/strips");
      appEl.innerHTML = (data || []).map(stripCard).join("") || "<div class='muted'>No strips configured.</div>";
      statusEl.textContent = "Updated: " + new Date().toLocaleTimeString();
    } catch (e) {
      statusEl.textContent = "Error";
      errEl.textContent = e?.message || String(e);
      appEl.innerHTML = "";
    }
  }

  async function toggleOutlet(stripId, idx) {
    try {
      await apiPost(`/v1/strips/${encodeURIComponent(stripId)}/outlets/${idx}/toggle`);
      await refresh();
    } catch (e) {
      errEl.textContent = e?.message || String(e);
    }
  }

  async function setOutlet(stripId, idx, op) {
    try {
      await apiPost(`/v1/strips/${encodeURIComponent(stripId)}/outlets/${idx}/${op}`);
      await refresh();
    } catch (e) {
      errEl.textContent = e?.message || String(e);
    }
  }

  async function allOff(stripId) {
    try {
      await apiPost(`/v1/strips/${encodeURIComponent(stripId)}/all/off`);
      await refresh();
    } catch (e) {
      errEl.textContent = e?.message || String(e);
    }
  }

  loadToken();
  refresh();
</script>
</body>
</html>
"""

def require_auth(authorization: str | None = Header(default=None)) -> None:
    """
    Bearer-token authentication.
    If KS300_API_TOKEN is unset, auth is disabled (useful for dev).
    """
    if not API_TOKEN:
        return

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
        )

    token = authorization.removeprefix("Bearer ").strip()
    if token != API_TOKEN:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid bearer token",
        )

def _parse_allowlist(raw: str) -> list[ipaddress._BaseNetwork]:
    """
    Parse comma-separated IPs or CIDRs into ipaddress networks.
    Single IPs are treated as /32 or /128.
    """
    nets: list[ipaddress._BaseNetwork] = []
    if not raw:
        return nets

    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue

        try:
            if "/" in part:
                nets.append(ipaddress.ip_network(part, strict=False))
            else:
                ip = ipaddress.ip_address(part)
                prefix = 32 if ip.version == 4 else 128
                nets.append(ipaddress.ip_network(f"{ip}/{prefix}", strict=False))
        except ValueError:
            raise RuntimeError(f"Invalid KS300_ALLOWLIST entry: {part}")

    return nets


ALLOWLIST = _parse_allowlist(ALLOWLIST_RAW)

def require_allowlist(request: Request) -> None:
    """
    Enforce client IP allowlist.
    Uses direct socket peer only (no X-Forwarded-For).
    """
    if not ALLOWLIST:
        return  # allowlist disabled

    if not request.client or not request.client.host:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Unable to determine client IP",
        )

    ip_str = request.client.host
    try:
        ip = ipaddress.ip_address(ip_str)
    except ValueError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=f"Invalid client IP: {ip_str}",
        )

    if not any(ip in net for net in ALLOWLIST):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Client IP not allowed",
        )

app = FastAPI(title="jetkvm-tplink-ks300-local")

v1 = APIRouter(
    prefix="/v1",
    dependencies=[Depends(require_allowlist), Depends(require_auth)],
)

@dataclass(frozen=True)
class StripCfg:
    id: str
    host: str
    name: str
    outlets: List[Dict[str, Any]]


def load_config() -> List[StripCfg]:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}

    strips: List[StripCfg] = []
    for s in cfg.get("strips", []):
        strips.append(
            StripCfg(
                id=s["id"],
                host=s["host"],
                name=s.get("name", s["id"]),
                outlets=s.get("outlets", []),
            )
        )
    return strips


STRIPS = load_config()

class OutletState(BaseModel):
    index: int
    name: Optional[str] = None
    is_on: bool
    power_w: Optional[float] = None
    energy_wh: Optional[float] = None


class StripState(BaseModel):
    id: str
    name: str
    host: str
    outlets: List[OutletState]

async def get_strip_device(host: str):
    dev = await Discover.discover_single(host)
    if dev is None:
        raise HTTPException(
            status_code=404,
            detail=f"Device not found at {host}",
        )
    await dev.update()
    return dev


def outlet_name(cfg: StripCfg, idx: int) -> Optional[str]:
    for o in cfg.outlets:
        if int(o.get("index")) == idx:
            return o.get("name")
    return None


async def read_outlets(cfg: StripCfg) -> StripState:
    dev = await get_strip_device(cfg.host)

    children = getattr(dev, "children", None)
    if not children:
        raise HTTPException(
            status_code=400,
            detail="Device does not expose outlets (children)",
        )

    outlets: List[OutletState] = []
    for i, child in enumerate(children):
        await child.update()

        st = OutletState(
            index=i,
            name=outlet_name(cfg, i) or getattr(child, "alias", None),
            is_on=bool(getattr(child, "is_on", False)),
        )

        try:
            em = getattr(child, "emeter_realtime", None)
            if isinstance(em, dict):
                if "power" in em:
                    st.power_w = float(em["power"])
                elif "power_mw" in em:
                    st.power_w = float(em["power_mw"]) / 1000.0
        except Exception:
            pass

        outlets.append(st)

    return StripState(
        id=cfg.id,
        name=cfg.name,
        host=cfg.host,
        outlets=outlets,
    )

async def set_outlet(
    cfg: StripCfg,
    idx: int,
    state: Optional[bool],
    toggle: bool = False,
) -> OutletState:
    dev = await get_strip_device(cfg.host)

    children = getattr(dev, "children", None)
    if not children or idx < 0 or idx >= len(children):
        raise HTTPException(
            status_code=404,
            detail=f"Outlet index {idx} not found",
        )

    child = children[idx]
    await child.update()

    if toggle:
        if getattr(child, "is_on", False):
            await child.turn_off()
        else:
            await child.turn_on()
    else:
        if state is True:
            await child.turn_on()
        elif state is False:
            await child.turn_off()
        else:
            raise HTTPException(
                status_code=400,
                detail="state must be true/false for on/off",
            )

    await child.update()

    return OutletState(
        index=idx,
        name=outlet_name(cfg, idx) or getattr(child, "alias", None),
        is_on=bool(getattr(child, "is_on", False)),
    )

def cfg_by_id(strip_id: str) -> StripCfg:
    for s in STRIPS:
        if s.id == strip_id:
            return s
    raise HTTPException(
        status_code=404,
        detail=f"Unknown strip id: {strip_id}",
    )

@app.get("/healthz")
async def healthz():
    return {"ok": True}


@v1.get("/strips", response_model=List[StripState])
async def list_strips():
    tasks = [read_outlets(cfg) for cfg in STRIPS]
    return await asyncio.gather(*tasks)


@v1.post("/strips/{strip_id}/outlets/{index}/on", response_model=OutletState)
async def outlet_on(strip_id: str, index: int):
    return await set_outlet(cfg_by_id(strip_id), index, True)


@v1.post("/strips/{strip_id}/outlets/{index}/off", response_model=OutletState)
async def outlet_off(strip_id: str, index: int):
    return await set_outlet(cfg_by_id(strip_id), index, False)


@v1.post("/strips/{strip_id}/outlets/{index}/toggle", response_model=OutletState)
async def outlet_toggle(strip_id: str, index: int):
    return await set_outlet(cfg_by_id(strip_id), index, None, toggle=True)

@v1.post("/strips/{strip_id}/all/off")
async def all_off(strip_id: str):
    cfg = cfg_by_id(strip_id)
    dev = await get_strip_device(cfg.host)
    children = getattr(dev, "children", None) or []
    await asyncio.gather(*[c.turn_off() for c in children])
    return {"ok": True}

@app.get("/", response_class=HTMLResponse)
async def ui():
    return HTMLResponse(UI_HTML)

app.include_router(v1)