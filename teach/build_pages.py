import os
import subprocess
from bs4 import BeautifulSoup


def convert_notebook_to_html(notebook_path, output_dir, output_file):
    """Convert a Jupyter notebook to HTML using nbconvert."""
    subprocess.run(
        [
            "jupyter",
            "nbconvert",
            "--to",
            "html",
            "--output-dir",
            output_dir,
            "--output",
            output_file,
            notebook_path,
        ]
    )


def add_thebe_to_html(html_path):
    """Modify the HTML to integrate Thebe for interactive code execution."""
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Add CodeMirror CSS first (preload for seamless styling)
    codemirror_css = soup.new_tag(
        "link", rel="stylesheet", href="https://unpkg.com/codemirror@5.65.16/lib/codemirror.css"
    )
    soup.head.append(codemirror_css)

    # Add Thebe CSS to head
    css_link = soup.new_tag(
        "link", rel="stylesheet", href="https://unpkg.com/thebe@latest/dist/thebe.css"
    )
    soup.head.append(css_link)
    
    # Add custom CSS to match pre and post-activation appearance
    custom_style = soup.new_tag("style")
    custom_style.string = """
    /* Override Jupyter nbconvert styling to match CodeMirror */
    .jp-InputArea-editor,
    .highlight,
    div.highlight,
    .jp-Cell-inputWrapper,
    .jp-InputPrompt,
    div.input_area,
    div.highlight pre {
        font-family: Menlo, Consolas, 'Courier New', monospace !important;
        font-size: 14px !important;
        line-height: 1.4 !important;
        background: #f5f5f5 !important;
        margin: 0 !important;
    }
    
    /* Style the actual pre elements inside highlights */
    div.highlight pre,
    .highlight pre,
    pre[data-executable] {
        font-family: Menlo, Consolas, 'Courier New', monospace !important;
        font-size: 14px !important;
        line-height: 1.4 !important;
        background: #f5f5f5 !important;
        padding: 0px !important;
        overflow: auto !important;
        white-space: pre !important;
        margin: 0 !important;
    }
    
    /* Remove Jupyter's default prompt styling */
    .jp-InputPrompt {
        display: none !important;
    }
    
    /* Clean up cell containers */
    .jp-Cell,
    .jp-CodeCell,
    .jp-InputArea {
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
    }
    
    /* Match CodeMirror to the same styling */
    .CodeMirror {
        font-family: Menlo, Consolas, 'Courier New', monospace !important;
        font-size: 14px !important;
        line-height: 1.4 !important;
        background: #f5f5f5 !important;
        padding: 8px !important;
        border: 1px solid #ddd !important;
        height: auto !important;
        margin: 0 !important;
    }
    
    .CodeMirror-scroll {
        overflow: auto !important;
    }
    
    .CodeMirror pre {
        font-family: Menlo, Consolas, 'Courier New', monospace !important;
        font-size: 14px !important;
        line-height: 1.4 !important;
        padding-left: 0 !important;
    }
    
    /* Hide line numbers completely */
    .CodeMirror-linenumber,
    .CodeMirror-gutter,
    .CodeMirror-gutters {
        display: none !important;
        width: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Ensure code doesn't shift when editor activates */
    .CodeMirror-lines {
        padding: 0 !important;
    }
    
    .CodeMirror-line {
        padding-left: 0 !important;
        padding-right: 0 !important;
        border: none !important;
        background: transparent !important;
    }
    
    /* Remove line borders and backgrounds */
    .CodeMirror-linebackground {
        display: none !important;
    }
    
    .CodeMirror-code {
        border: none !important;
    }
    
    /* Ensure no layout shift */
    .thebe-cell {
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
    }
    
    .thebe-input {
        overflow: auto !important;
    }
    
    /* Ensure editors remain selectable and interactive (apply to internals) */
    .CodeMirror,
    .CodeMirror * ,
    .CodeMirror textarea,
    .CodeMirror pre,
    div.highlight pre,
    pre[data-executable],
    .thebe-input {
        -webkit-user-select: text !important;
        -moz-user-select: text !important;
        -ms-user-select: text !important;
        user-select: text !important;
        -webkit-user-drag: text !important;
        pointer-events: auto !important;
        caret-color: auto !important;
    }

    /* Some CodeMirror themes set unselectable on line spans; ensure lines are selectable */
    .CodeMirror-line,
    .CodeMirror-code,
    .CodeMirror-line * {
        -webkit-user-select: text !important;
        -moz-user-select: text !important;
        -ms-user-select: text !important;
        user-select: text !important;
    }

    /* Remove any syntax highlighting colors for consistency */
    .highlight .k,
    .highlight .n,
    .highlight .o,
    .highlight .p,
    .highlight .s,
    .highlight .nb,
    .highlight .mi,
    .highlight .mf {
        color: inherit !important;
    }
    """
    soup.head.append(custom_style)

    # Add Thebe JS to head
    js_script = soup.new_tag(
        "script",
        type="text/javascript",
        src="https://unpkg.com/thebe@latest/lib/index.js",
    )
    soup.head.append(js_script)

    # Add Thebe config script to body
    config_script = soup.new_tag("script", type="text/x-thebe-config")
    config_script.string = """{
        "bootstrap": false,
        "useBinder": false,
        "useJupyterLite": false,
        "requestKernel": true,
        "serverSettings": {
            "baseUrl": "http://localhost:8888",
            "token": "test-secret",
            "appendToken": true
        },
        "kernelOptions": {
            "name": "python",
            "kernelName": "python"
        },
        "mountActivateWidget": true,
        "mountStatusWidget": true,
        "mountRunButton": true,
        "mountRunAllButton": false,
        "mountRestartButton": false,
        "mountRestartAllButton": false,
        "codeMirrorConfig": {
            "theme": "default",
            "lineNumbers": false,
            "readOnly": false,
            "styleActiveLine": false,
            "matchBrackets": false,
            "autoRefresh": false
        },
        "preRenderHook": function() {
            document.querySelectorAll("pre[data-executable]").forEach(function(el) {
                var height = el.getBoundingClientRect().height;
                el.style.minHeight = height + "px";
            });
        }
    }"""
    soup.body.append(config_script)

    # Add script to handle buttons
    button_script = soup.new_tag("script")
    button_script.string = """
    document.getElementById('restart-kernel').addEventListener('click', function() {
        if (window.thebe) {
            window.thebe.restart();
        }
    });
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('run-cell')) {
            if (window.thebe) {
                const pre = e.target.nextElementSibling;
                if (pre && pre.tagName === 'PRE') {
                    window.thebe.runCell(pre);
                }
            }
        }
    });
    """
    soup.body.append(button_script)

    # Modify code cells to be executable with Thebe
    for pre in soup.find_all("pre"):
        # Check if it's a code cell (inside div.highlight)
        if (
            pre.parent
            and pre.parent.name == "div"
            and "highlight" in pre.parent.get("class", [])
        ):
            pre["data-executable"] = "true"
            pre["data-language"] = "python"

    # Add Thebe activate and status widgets (insert at the beginning of body)
    activate_div = soup.new_tag("div", **{"class": "thebe-activate"})
    status_div = soup.new_tag("div", **{"class": "thebe-status"})
    restart_button = soup.new_tag("button", id="restart-kernel")
    restart_button.string = "Restart Kernel"
    soup.body.insert(0, restart_button)
    soup.body.insert(0, status_div)
    soup.body.insert(0, activate_div)

    # Write back the modified HTML
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(str(soup))


def main():
    # Create pages directory if it doesn't exist
    os.makedirs("pages", exist_ok=True)

    # Process all notebooks in the notebooks folder
    for file in os.listdir("notebooks"):
        if file.endswith(".ipynb"):
            base_name = file[:-6]  # Remove .ipynb extension
            html_file = f"pages/{base_name}.html"
            notebook_path = f"notebooks/{file}"

            # Convert notebook to HTML
            convert_notebook_to_html(notebook_path, "pages", f"{base_name}.html")

            # Add Thebe integration
            add_thebe_to_html(html_file)

            print(f"Converted {file} to {html_file} with Thebe integration")


if __name__ == "__main__":
    main()
