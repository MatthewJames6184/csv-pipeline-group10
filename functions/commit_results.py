import subprocess
import os

def commit_results_to_repository():
    try:
        # Check if we're in a git repository
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True, text=True
        )
        
        if result.returncode != 0:
            print("Not in a git repository. Skipping commit.")
            return
        
        # Add output and versions folders
        subprocess.run(["git", "add", "output/"], check=True)
        subprocess.run(["git", "add", "versions/"], check=True)
        
        # Commit changes
        result = subprocess.run(
            ["git", "commit", "-m", "Auto: commit processed output files [skip ci]"],
            capture_output=True, text=True
        )
        
        # Check commit result
        if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
            print("Nothing new to commit.")
        else:
            # Push changes
            push_result = subprocess.run(
                ["git", "push"],
                capture_output=True, text=True
            )
            
            if push_result.returncode == 0:
                print("✅ Results committed and pushed.")
            else:
                print(f"Push failed: {push_result.stderr}")
                
    except subprocess.CalledProcessError as e:
        print(f"Git error (expected in CI, safe to ignore): {e}")
    except FileNotFoundError:
        print("Git command not found. Skipping commit.")