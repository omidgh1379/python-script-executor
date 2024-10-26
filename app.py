from flask import Flask, request, jsonify, render_template
import json
import tempfile
import subprocess
import os
import textwrap

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    """Serve the HTML page to upload and execute scripts."""
    return render_template('index.html')

def execute_with_nsjail(user_script):
    # Wrapper code to call main() and serialize the result
    wrapper_code = textwrap.dedent("""\
    import json

    try:
        result = main()
        if not isinstance(result, (dict, list)):
            raise ValueError("main() must return a JSON object (dict or list).")
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
    """)

    # Combine the user's script with the wrapper code
    full_script = f"{user_script}\n{wrapper_code}"

    try:
        # Create a temporary file to store the combined script
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False, dir='/tmp') as temp_script:
            temp_script.write(full_script.encode('utf-8'))
            temp_script_path = temp_script.name

        # Ensure the temporary file is readable and executable
        os.chmod(temp_script_path, 0o755)

        # Define the nsjail command
        nsjail_command = [
    "/usr/local/bin/nsjail",
    "--mode", "o",
    "--max_cpus", "1",
    "--time_limit", "10",
    "--disable_clone_newnet",
    "--disable_clone_newuser",
    "--disable_clone_newns",
    "--disable_clone_newpid",
    "--disable_clone_newipc",
    "--disable_clone_newuts",
    "--disable_clone_newcgroup",
    "--cwd", "/",
    "--chroot", "/",
    "--bindmount_ro", "/usr",
    "--bindmount_ro", "/lib",
    "--bindmount_ro", "/lib64",
    "--bindmount_ro", "/bin",
    "--proc_path", "/proc",
    "--rlimit_as", "700",
    "--rlimit_cpu", "5",
    "--",
    "/usr/bin/python3", temp_script_path
]

        # Execute the script using nsjail
        result = subprocess.run(nsjail_command, capture_output=True, text=True)

        # Clean up the temporary script file
        os.remove(temp_script_path)

        # Check for errors in nsjail execution
        if result.returncode != 0:
            error_msg = result.stderr.strip() or result.stdout.strip()
            raise Exception(f"Error executing script: {error_msg}")

        # Parse the output as JSON
        output = json.loads(result.stdout.strip())

        # Check if the output contains an error
        if 'error' in output:
            raise Exception(output['error'])

        return output

    except json.JSONDecodeError as e:
        raise Exception(f"Invalid JSON output: {e}")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")
    finally:
        # Ensure the temporary script file is removed
        if os.path.exists(temp_script_path):
            os.remove(temp_script_path)

@app.route('/execute', methods=['POST'])
def execute_script():
    try:
        data = request.get_json()

        if not data or 'script' not in data:
            return jsonify({"error": "No script provided in the request body."}), 400

        script = data['script']

        # Ensure that the script contains a 'main()' function
        if 'def main' not in script:
            return jsonify({"error": "The script must contain a 'main()' function."}), 400

        # Execute the script using nsjail and capture the result
        result = execute_with_nsjail(script)

        return jsonify({"result": result}), 200

    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format in script output."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
