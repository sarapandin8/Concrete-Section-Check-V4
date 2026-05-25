"""Concrete PMM Pro Streamlit application."""

from __future__ import annotations

import streamlit as st

from concrete_pmm_pro.ui.analysis_page import render_analysis_page
from concrete_pmm_pro.ui.loads_page import render_loads_page
from concrete_pmm_pro.ui.materials_page import render_materials_page
from concrete_pmm_pro.ui.prestress_page import render_prestress_page
from concrete_pmm_pro.ui.project_page import render_project_page
from concrete_pmm_pro.ui.rebar_page import render_rebar_page
from concrete_pmm_pro.ui.section_builder import render_section_builder


WORKSPACE_NAVIGATION = {
    "Setup": ["Project", "Materials"],
    "Sections": ["Section Builder", "Rebar", "Prestress"],
    "Loads": ["Loads"],
    "Analysis": ["ULS / PMM", "SLS / Stress & Cracking", "Report / QA"],
    "Results": ["Results"],
}

RESULTS_WORKSPACE_PLACEHOLDER = (
    "Future Results Workspace. Current result outputs remain available under Analysis. "
    "Future milestones will add Summary Table, Case Details, Interaction Diagram, Charts, and Report Preview."
)


def _format_section_dimensions(parameters: dict | None) -> str:
    if not parameters:
        return ""

    width = parameters.get("width_mm")
    height = parameters.get("height_mm") or parameters.get("depth_mm")
    diameter = parameters.get("diameter_mm")
    outer_diameter = parameters.get("outer_diameter_mm")

    if width is not None and height is not None:
        return f"{float(width):,.0f} × {float(height):,.0f} mm"
    if diameter is not None:
        return f"D {float(diameter):,.0f} mm"
    if outer_diameter is not None:
        return f"Do {float(outer_diameter):,.0f} mm"
    return ""


def _active_section_summary() -> str:
    section_geometry = st.session_state.get("section_geometry")
    if section_geometry is None:
        return "Not defined"

    preset_name = st.session_state.get("section_preset_name", "Section")
    dimensions = _format_section_dimensions(st.session_state.get("section_parameters"))
    return f"{preset_name} {dimensions}".strip()


def _workflow_indicator(label: str, ready: bool | None) -> str:
    if ready is True:
        mark = "✓"
    elif ready is False:
        mark = "⚠"
    else:
        mark = "○"
    return f"{mark} {label}"


def _last_analysis_summary() -> str:
    status = st.session_state.get("analysis_runtime_cache_status") or st.session_state.get("analysis_runtime_last_status")
    if not status:
        return "Not run"

    last_run_at = st.session_state.get("analysis_runtime_last_run_at")
    last_time = st.session_state.get("analysis_runtime_last_time_seconds")
    parts = [str(status)]
    if last_time is not None:
        parts.append(f"{float(last_time):.2f} s")
    if last_run_at:
        parts.append(str(last_run_at))
    return " · ".join(parts)


def render_sidebar_status_panel() -> None:
    with st.sidebar:
        st.markdown("### Concrete PMM Pro")
        st.caption("Model status")

        st.markdown("#### Project")
        st.write(st.session_state.get("project_name", "Untitled Project"))

        st.markdown("#### Active Section")
        st.write(_active_section_summary())

        st.markdown("#### Workflow Status")
        has_materials = bool(st.session_state.get("design_code") or st.session_state.get("concrete_material"))
        has_section = st.session_state.get("section_geometry") is not None
        has_rebar_state = st.session_state.get("rebars_valid_for_analysis")
        has_prestress_state = st.session_state.get("prestress_valid_for_analysis")
        has_loads = bool(st.session_state.get("load_cases"))
        has_pmm = st.session_state.get("rc_pmm_result") is not None
        has_report = st.session_state.get("report_manifest") is not None

        st.write(_workflow_indicator("Setup", bool(st.session_state.get("project_name"))))
        st.write(_workflow_indicator("Materials", has_materials))
        st.write(_workflow_indicator("Section", has_section))
        st.write(_workflow_indicator("Rebar", has_rebar_state if has_rebar_state is not None else None))
        st.write(_workflow_indicator("Prestress", has_prestress_state if has_prestress_state is not None else None))
        st.write(_workflow_indicator("Loads", has_loads))
        st.write(_workflow_indicator("Analysis", has_pmm))
        st.write(_workflow_indicator("Report", has_report))

        st.markdown("#### Current Mode")
        st.write("Column / Pier / Wall / Pylon - PMM Mode")

        st.markdown("#### Last Analysis")
        st.write(_last_analysis_summary())


def render_setup_workspace() -> None:
    project_tab, materials_tab = st.tabs(WORKSPACE_NAVIGATION["Setup"])
    with project_tab:
        render_project_page()
    with materials_tab:
        render_materials_page()


def render_sections_workspace() -> None:
    section_tab, rebar_tab, prestress_tab = st.tabs(WORKSPACE_NAVIGATION["Sections"])
    with section_tab:
        render_section_builder()
    with rebar_tab:
        render_rebar_page()
    with prestress_tab:
        render_prestress_page()


def render_loads_workspace() -> None:
    render_loads_page()


def render_analysis_workspace() -> None:
    render_analysis_page()


def render_results_workspace() -> None:
    st.info(RESULTS_WORKSPACE_PLACEHOLDER)


def main() -> None:
    st.set_page_config(page_title="Concrete PMM Pro", layout="wide")
    render_sidebar_status_panel()
    st.title("Concrete PMM Pro")
    st.caption(
        "Milestone UI.A0.1: sidebar cleanup and model status panel. "
        "Internal units: mm, MPa, N, N-mm."
    )

    setup_tab, sections_tab, loads_tab, analysis_tab, results_tab = st.tabs(list(WORKSPACE_NAVIGATION.keys()))
    with setup_tab:
        render_setup_workspace()
    with sections_tab:
        render_sections_workspace()
    with loads_tab:
        render_loads_workspace()
    with analysis_tab:
        render_analysis_workspace()
    with results_tab:
        render_results_workspace()


if __name__ == "__main__":
    main()
