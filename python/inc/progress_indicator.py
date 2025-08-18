import time

def show_progress(current, total, start_time, operation_name="Operation", unit="MB"):
    """Reusable progress indicator function."""
    progress = current / total
    bar_length = 50
    filled_length = int(bar_length * progress)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    percent = progress * 100
    
    # Calculate elapsed time and estimated time remaining
    elapsed_time = time.time() - start_time
    if progress > 0:
        estimated_total_time = elapsed_time / progress
        eta = estimated_total_time - elapsed_time
    else:
        eta = 0
    
    # Format time as mm:ss
    elapsed_str = f"{int(elapsed_time//60):02d}:{int(elapsed_time%60):02d}"
    eta_str = f"{int(eta//60):02d}:{int(eta%60):02d}"
    
    # Speed calculation
    if unit == "MB":
        current_mb = current / (1024 * 1024)
        total_mb = total / (1024 * 1024)
        speed_kbps = (current_mb * 1024) / elapsed_time if elapsed_time > 0 else 0
        size_info = f"({current_mb:.1f}{unit}/{total_mb:.1f}{unit})"
        speed_info = f"({speed_kbps:.1f}KB/s)"
    else:
        speed_kbps = current / elapsed_time if elapsed_time > 0 else 0
        size_info = f"({current}{unit}/{total}{unit})"
        speed_info = f"({speed_kbps:.1f}/s)"
    
    # Print progress on two lines
    print(f'\r[{bar}] {percent:.1f}%', end='')
    print(f'\n{size_info} {elapsed_str} elapsed, ETA {eta_str} {speed_info}', end='')
    print('\033[A', end='', flush=True)  # Move cursor up one line for next update
