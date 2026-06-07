# AI Usage Note

## 1. What AI Helped With During Development
* **Architectural Scaffolding:** The AI assistant was instrumental in generating the initial boilerplate code for the Streamlit dashboard and establishing a modular, maintainable project structure (e.g., separating `sql_generator.py`, `validator.py`, and `app.py`).
* **UI/UX Refinement:** AI helped resolve responsive layout challenges in Streamlit. For example, it calculated optimal column ratios and applied vertical alignment properties to seamlessly align interactive widgets with text headers.
* **Data Visualization Styling:** The assistant significantly enhanced the aesthetics of the Plotly charts by providing syntax for advanced configurations, such as spline interpolation for line charts, dynamic category mapping for scatter plots, and adjusted marker opacities.
* **Automated Testing & Debugging:** The AI was utilized to rapidly debug Python stack traces (such as `IndentationError` and `ModuleNotFoundError`) and to consolidate disparate unit tests into a single, comprehensive `pytest` suite, ensuring robust validation of the SQL pipeline.
* **Security Implementation:** AI assisted in formulating the string matching logic for the SQL validator to ensure that destructive DDL/DML queries were safely blocked before execution.

## 2. What AI Got Wrong or Struggled With
* **Stale Context & Phantom Files:** The AI occasionally struggled with context retention when project files were structurally modified. For example, it attempted to run tests on a `confidence_score.py` module that had already been removed from the repository, requiring manual intervention to correct its contextual awareness.
* **Visual Proportions:** Initially, the AI struggled to intuitively grasp visual spacing constraints without explicit mathematical guidance. It suggested column ratios that left disproportionate white space in the UI, requiring iterative prompting to achieve the correct, tight visual alignment.
* **Schema Hallucinations in Text-to-SQL:** When designing the core LLM integration, we observed that if the AI was not strictly bounded by an injected database schema, it would frequently hallucinate table names and foreign keys. This required us to manually engineer a `schema_tool.py` to ground the LLM's generation context.

## 3. Best Prompts Used
Here are some of the most effective and structured prompts utilized to steer the AI assistant during development:

1. **Prompt for UI Alignment:** *"Analyze the current Streamlit column layout for the chart selector. The spacing between the subheader and the dropdown is too wide. Please adjust the column ratios and apply vertical alignment to center them seamlessly."*
   > **Impact:** This forced the AI to abandon default Streamlit spacing and utilize precise `st.columns` parameters to fix the UI layout.

2. **Prompt for Automated Testing:** *"Review the stack trace from the failing pytest suite in test_agent.py. Identify the root cause of the ModuleNotFoundError and refactor the test file to comprehensively cover only the currently active modules."*
   > **Impact:** A highly effective prompt that directed the AI to autonomously debug module import errors and clean up the test suite without requiring manual code pasting.

3. **Prompt for Advanced Visualizations:** *"Enhance the Plotly line and scatter charts in chart_generator.py. Apply professional styling including spline curves for lines, larger marker sizes, and dynamic color mapping based on categorical columns."*
   > **Impact:** This prompt abstracted away the complex Plotly syntax, allowing the AI to generate production-ready visualization configurations efficiently.

4. **Prompt for Requirements Validation:** *"Evaluate the entire project repository against the provided grading rubric. Identify any missing deliverables such as documentation, sample outputs, or unhandled test cases."*
   > **Impact:** Effectively repurposed the AI from a coding assistant into an automated compliance checker to ensure all mandatory submission requirements were met.


