import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


def generate_pdf_report(all_results):
    """Generate a simple PDF report with scan findings."""
    
    # Create output directory if it doesn't exist
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"risk_assessment_report_{timestamp}.pdf"
    output_path = os.path.join(output_dir, filename)
    
    # Create PDF document
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    story.append(Paragraph("Security Risk Assessment Report", styles['Title']))
    story.append(Spacer(1, 0.2*inch))
    
    # Date and summary
    report_date = datetime.now().strftime("%B %d, %Y %H:%M:%S")
    story.append(Paragraph(f"Generated: {report_date}", styles['Normal']))
    story.append(Paragraph(f"Total Assets: {len(all_results)}", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Results for each asset
    for idx, result in enumerate(all_results, 1):
        asset = result["asset"]
        scan_result = result["scan_result"]
        risk_result = result["risk_result"]
        
        # Asset header
        story.append(Paragraph(f"Asset {idx}: {asset['ip']}", styles['Heading2']))
        
        # Asset details
        story.append(Paragraph(f"Type: {asset['asset_type'].upper()}", styles['Normal']))
        story.append(Paragraph(f"Zone: {asset['zone'].upper()}", styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
        
        # Scan results
        if "error" in scan_result:
            story.append(Paragraph(f"Status: ERROR - {scan_result['error']}", styles['Normal']))
        else:
            open_ports = scan_result.get("open_ports", [])
            if open_ports:
                ports_str = ", ".join([f"{p['port']} ({p['service']})" for p in open_ports])
                story.append(Paragraph(f"Open Ports: {ports_str}", styles['Normal']))
            else:
                story.append(Paragraph("Open Ports: None", styles['Normal']))
            
            # Risk assessment
            if risk_result:
                story.append(Paragraph(f"Risk Level: {risk_result['risk_level']}", styles['Normal']))
                
                findings = risk_result.get("findings", [])
                if findings:
                    story.append(Paragraph("Findings:", styles['Normal']))
                    for finding in findings:
                        story.append(Paragraph(f"  • {finding}", styles['Normal']))
        
        story.append(Spacer(1, 0.2*inch))
    
    # Build PDF
    doc.build(story)
    
    return output_path