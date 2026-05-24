"""Low-level figure export helpers for future report generation."""

from __future__ import annotations

from typing import Any


def plotly_figure_to_html_bytes(fig: Any) -> bytes:
    """Return standalone Plotly HTML bytes for an existing figure."""

    return fig.to_html(full_html=True, include_plotlyjs="cdn").encode("utf-8")


def plotly_figure_to_png_bytes(fig: Any) -> tuple[bytes | None, list[str]]:
    """Return PNG bytes when static image export is available.

    Plotly PNG export requires kaleido. The app should continue to work when
    kaleido is absent, so failures are returned as warnings instead of raised.
    """

    try:
        return fig.to_image(format="png"), []
    except (ImportError, ValueError, RuntimeError, OSError) as exc:
        return None, [f"PNG export requires kaleido. HTML export remains available. Detail: {exc}"]
