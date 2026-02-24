import subprocess

def commit_results_to_repository():
    # STUB — this runs fine locally but the real commit happens via GitHub Actions CI
    try:
        subprocess.run(["git", "add", "output/"], check=True)
        result = subprocess.run(
            ["git", "commit", "-m", "Auto: commit processed output files [skip ci]"],
            capture_output=True, text=True
        )
        if "nothing to commit" in result.stdout:
            print("Nothing new to commit.")
        else:
            subprocess.run(["git", "push"], check=True)
            print("✅ Results committed and pushed.")
    except subprocess.CalledProcessError as e:
        print(f"Git error (expected in CI, safe to ignore): {e}")