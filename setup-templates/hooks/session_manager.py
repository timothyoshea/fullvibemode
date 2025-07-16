#!/usr/bin/env python3
"""
Advanced session manager for Claude Code
"""
import sys
import json
import os
import subprocess
import platform
from datetime import datetime

def send_notification(title, message, sound="Glass"):
    """Send system notification"""
    if platform.system() == "Darwin":  # macOS
        script = f'display notification "{message}" with title "{title}" sound name "{sound}"'
        subprocess.run(["osascript", "-e", script], capture_output=True)

def generate_session_report(data):
    """Generate comprehensive session report"""
    
    total_tools = data.get("total_tools_used", 0)
    duration_ms = data.get("duration_ms", 0)
    duration_min = duration_ms / 60000 if duration_ms > 0 else 0
    
    # Load usage statistics
    stats_file = os.path.join(os.path.dirname(__file__), '../logs/stats.json')
    tool_breakdown = {}
    
    try:
        if os.path.exists(stats_file):
            with open(stats_file, 'r') as f:
                stats = json.load(f)
                tool_breakdown = stats.get("tool_counts", {})
    except Exception:
        pass
    
    # Generate report
    report = {
        "session_end": datetime.now().isoformat(),
        "duration_minutes": round(duration_min, 1),
        "total_tools_used": total_tools,
        "tools_per_minute": round(total_tools / duration_min, 1) if duration_min > 0 else 0,
        "tool_breakdown": tool_breakdown,
        "session_summary": {
            "productivity_score": calculate_productivity_score(total_tools, duration_min),
            "automation_efficiency": calculate_automation_efficiency(tool_breakdown),
            "most_used_tool": max(tool_breakdown.items(), key=lambda x: x[1])[0] if tool_breakdown else "none"
        }
    }
    
    return report

def calculate_productivity_score(total_tools, duration_min):
    """Calculate productivity score based on tool usage"""
    if duration_min == 0:
        return 0
    
    tools_per_minute = total_tools / duration_min
    
    # Score based on tools per minute (optimal range: 1-3)
    if tools_per_minute < 0.5:
        return "low"
    elif tools_per_minute < 1.5:
        return "moderate"
    elif tools_per_minute < 3:
        return "high"
    else:
        return "very_high"

def calculate_automation_efficiency(tool_breakdown):
    """Calculate automation efficiency score"""
    if not tool_breakdown:
        return "no_data"
    
    # Automated tools vs manual tools
    automated_tools = ["bash", "write", "edit", "multi_edit"]
    manual_tools = ["read", "grep", "glob"]
    
    automated_count = sum(tool_breakdown.get(tool, 0) for tool in automated_tools)
    manual_count = sum(tool_breakdown.get(tool, 0) for tool in manual_tools)
    
    if automated_count == 0 and manual_count == 0:
        return "no_data"
    
    automation_ratio = automated_count / (automated_count + manual_count)
    
    if automation_ratio < 0.3:
        return "low_automation"
    elif automation_ratio < 0.6:
        return "moderate_automation"
    else:
        return "high_automation"

def save_session_report(report):
    """Save session report to file"""
    
    log_dir = os.path.join(os.path.dirname(__file__), '../logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Save detailed report
    report_file = os.path.join(log_dir, f"session_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    # Update session history
    history_file = os.path.join(log_dir, "session_history.json")
    
    try:
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)
        else:
            history = {"sessions": [], "total_sessions": 0}
        
        # Add current session
        history["sessions"].append({
            "timestamp": report["session_end"],
            "duration_minutes": report["duration_minutes"],
            "total_tools": report["total_tools_used"],
            "productivity_score": report["session_summary"]["productivity_score"],
            "automation_efficiency": report["session_summary"]["automation_efficiency"]
        })
        
        # Keep only last 50 sessions
        history["sessions"] = history["sessions"][-50:]
        history["total_sessions"] += 1
        
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)
            
    except Exception:
        pass  # Silently handle history errors

def create_final_checkpoint():
    """Create final git checkpoint if needed"""
    
    try:
        # Check if we're in a git repo and have changes
        result = subprocess.run(["git", "status", "--porcelain"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0 and result.stdout.strip():
            subprocess.run(["git", "add", "."], capture_output=True)
            
            commit_msg = f"""Session end checkpoint: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Final checkpoint from Claude Code session

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"""
            
            subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True)
            
    except Exception:
        pass  # Silently handle git errors

def send_session_summary(report):
    """Send session summary notification"""
    
    duration = report["duration_minutes"]
    tools_used = report["total_tools_used"]
    productivity = report["session_summary"]["productivity_score"]
    
    if duration < 1:
        message = f"Quick session: {tools_used} tools used"
    else:
        message = f"Session: {tools_used} tools in {duration}m ({productivity} productivity)"
    
    send_notification("📊 Session Complete", message, "Glass")

def main():
    try:
        data = json.load(sys.stdin)
        
        # Generate comprehensive session report
        report = generate_session_report(data)
        
        # Save report
        save_session_report(report)
        
        # Create final checkpoint
        create_final_checkpoint()
        
        # Send summary notification
        send_session_summary(report)
        
        # Return success with report data
        result = data.copy()
        result["session_report"] = report
        print(json.dumps(result))
        
    except Exception as e:
        # Log error but don't fail
        error_data = data if 'data' in locals() else {}
        error_data["session_manager_error"] = str(e)
        print(json.dumps(error_data))

if __name__ == "__main__":
    main()