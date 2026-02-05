#!/usr/bin/env python3
"""
Cuervo Competitive Social Media Intelligence Tool
==================================================
Main entry point. Generates templates, runs analysis on collected data,
and produces a multi-tab Excel dashboard.

Usage:
    python main.py templates    # Generate blank CSV templates for data collection
    python main.py demo         # Generate sample data + run full analysis + dashboard
    python main.py analyze      # Run analysis on your collected data + generate dashboard
    python main.py analyze --data-dir ./my_data  # Specify custom data directory
"""

import argparse
import os
import sys
from datetime import datetime


def cmd_templates(args):
    """Generate blank CSV templates for manual data collection."""
    from templates import generate_all_templates

    output_dir = args.output_dir or os.path.join(os.getcwd(), "cuervo_data")
    files = generate_all_templates(output_dir)

    print(f"\n{'='*60}")
    print("  CSV TEMPLATES GENERATED")
    print(f"{'='*60}")
    print(f"\n  Output directory: {output_dir}\n")
    for f in files:
        print(f"  - {os.path.basename(f)}")
    print(f"\n  Next steps:")
    print(f"  1. Read COLLECTION_GUIDE.md for instructions")
    print(f"  2. Populate the CSV files with real data")
    print(f"  3. Run: python main.py analyze --data-dir {output_dir}")
    print(f"{'='*60}\n")


def cmd_demo(args):
    """Generate sample data and run full analysis pipeline."""
    from sample_data import generate_all_sample_data
    from analysis import run_full_analysis
    from dashboard import generate_dashboard

    output_dir = args.output_dir or os.path.join(os.getcwd(), "cuervo_demo")
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n{'='*60}")
    print("  DEMO MODE — GENERATING SAMPLE DATA + ANALYSIS")
    print(f"{'='*60}\n")

    # Step 1: Generate sample data
    print("  [1/3] Generating sample data...")
    data_files = generate_all_sample_data(output_dir)
    for f in data_files:
        print(f"        - {os.path.basename(f)}")

    # Step 2: Run analysis
    print("\n  [2/3] Running competitive analysis...")
    results = run_full_analysis(output_dir)
    print(f"        - Analyzed {len(results['posts'])} posts across {len(set(p['brand'] for p in results['posts']))} brands")
    print(f"        - Generated {len(results['recommendations'])} recommendations")

    # Step 3: Generate dashboard
    dashboard_path = os.path.join(output_dir, f"cuervo_intelligence_report_{datetime.now().strftime('%Y%m%d')}.xlsx")
    print(f"\n  [3/3] Generating Excel dashboard...")
    generate_dashboard(results, dashboard_path)
    print(f"        - {os.path.basename(dashboard_path)}")

    # Summary
    print(f"\n{'='*60}")
    print("  ANALYSIS COMPLETE")
    print(f"{'='*60}")
    print(f"\n  Dashboard: {dashboard_path}")
    print(f"  Data dir:  {output_dir}")
    print(f"\n  Dashboard tabs:")
    print(f"    1. Executive Summary — Key findings + recommendations")
    print(f"    2. Brand Comparison  — Side-by-side metrics")
    print(f"    3. Content Strategy  — Theme/caption/CTA analysis")
    print(f"    4. Engagement Benchmarks — ER by content type + charts")
    print(f"    5. Hashtag Strategy  — Tag usage comparison")
    print(f"    6. Top Posts         — Best performing content per brand")
    print(f"    7. Posting Schedule  — Day/hour patterns")
    print(f"    8. Raw Data          — All post data for further analysis")

    high_recs = [r for r in results["recommendations"] if r["priority"] == "High"]
    if high_recs:
        print(f"\n  TOP HIGH-PRIORITY RECOMMENDATIONS FOR CUERVO:")
        for i, r in enumerate(high_recs[:5], 1):
            print(f"    {i}. [{r['platform']}] {r['recommendation']}")

    print(f"\n{'='*60}\n")


def cmd_analyze(args):
    """Run analysis on collected data."""
    from analysis import run_full_analysis
    from dashboard import generate_dashboard

    data_dir = args.data_dir or os.path.join(os.getcwd(), "cuervo_data")

    # Verify required files exist
    required_files = ["posts_data.csv", "brand_profiles.csv", "hashtag_tracking.csv", "creator_collabs.csv"]
    missing = [f for f in required_files if not os.path.exists(os.path.join(data_dir, f))]

    if missing:
        print(f"\n  ERROR: Missing required files in {data_dir}:")
        for f in missing:
            print(f"    - {f}")
        print(f"\n  Run 'python main.py templates' first to generate blank templates.")
        sys.exit(1)

    output_dir = args.output_dir or data_dir
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n{'='*60}")
    print("  RUNNING COMPETITIVE ANALYSIS")
    print(f"{'='*60}\n")

    print(f"  Data source: {data_dir}")
    print(f"\n  [1/2] Analyzing data...")
    results = run_full_analysis(data_dir)
    print(f"        - {len(results['posts'])} posts analyzed")
    print(f"        - {len(results['recommendations'])} recommendations generated")

    dashboard_path = os.path.join(output_dir, f"cuervo_intelligence_report_{datetime.now().strftime('%Y%m%d')}.xlsx")
    print(f"\n  [2/2] Generating dashboard...")
    generate_dashboard(results, dashboard_path)

    print(f"\n{'='*60}")
    print("  ANALYSIS COMPLETE")
    print(f"{'='*60}")
    print(f"\n  Dashboard: {dashboard_path}")

    high_recs = [r for r in results["recommendations"] if r["priority"] == "High"]
    if high_recs:
        print(f"\n  HIGH-PRIORITY RECOMMENDATIONS:")
        for i, r in enumerate(high_recs[:5], 1):
            print(f"    {i}. [{r['category']} | {r['platform']}]")
            print(f"       {r['insight']}")
            print(f"       → {r['recommendation']}")

    print(f"\n{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Cuervo Competitive Social Media Intelligence Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py templates                    Generate blank CSV templates
  python main.py demo                         Run with sample data
  python main.py analyze --data-dir ./data    Analyze your collected data
        """,
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Templates command
    p_templates = subparsers.add_parser("templates", help="Generate blank CSV templates")
    p_templates.add_argument("--output-dir", help="Output directory for templates")

    # Demo command
    p_demo = subparsers.add_parser("demo", help="Generate sample data + full analysis")
    p_demo.add_argument("--output-dir", help="Output directory")

    # Analyze command
    p_analyze = subparsers.add_parser("analyze", help="Analyze collected data")
    p_analyze.add_argument("--data-dir", help="Directory containing collected CSV data")
    p_analyze.add_argument("--output-dir", help="Output directory for dashboard")

    args = parser.parse_args()

    if args.command == "templates":
        cmd_templates(args)
    elif args.command == "demo":
        cmd_demo(args)
    elif args.command == "analyze":
        cmd_analyze(args)
    else:
        parser.print_help()
        print("\n  Start with: python main.py demo")


if __name__ == "__main__":
    main()
