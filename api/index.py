"""
Vercel Serverless Function Handler for Crew Management Dashboard
"""

from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Sample data for demo (Vercel serverless cannot read local files)
DEMO_DATA = {
    "summary": {
        "total_flights": 156,
        "total_block_hours": 312.5,
        "avg_flight_hours": 6.25,
        "total_aircraft": 50,
        "total_crew": 245,
        "multi_reg_count": 12,
        "crew_rotation_groups": 12
    },
    "aircraft": [],
    "crew_roles": {
        "PIC": 85,
        "FO": 92,
        "CC": 68
    },
    "multi_reg_crew": [],
    "utilization": {
        "A321": {"count": 30, "avg_hours": 6.5},
        "A320": {"count": 15, "avg_hours": 5.8},
        "A330": {"count": 5, "avg_hours": 8.2}
    },
    "rolling_stats": {
        "total_crew": 245,
        "avg_28day_hours": 65.2,
        "avg_365day_hours": 720.5
    },
    "crew_schedule": {
        "summary": {
            "standby": 15,
            "sick_call": 3,
            "fatigue": 2
        }
    }
}


@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    """Get all dashboard data"""
    return jsonify(DEMO_DATA)


@app.route('/api/summary', methods=['GET'])
def get_summary():
    """Get summary KPIs"""
    return jsonify(DEMO_DATA['summary'])


@app.route('/api/aircraft', methods=['GET'])
def get_aircraft():
    """Get aircraft list"""
    return jsonify({
        'total': DEMO_DATA['summary']['total_aircraft'],
        'avg_flight_hours': DEMO_DATA['summary']['avg_flight_hours'],
        'aircraft': DEMO_DATA['aircraft']
    })


@app.route('/api/crew', methods=['GET'])
def get_crew():
    """Get crew statistics"""
    return jsonify({
        'total': DEMO_DATA['summary']['total_crew'],
        'by_role': DEMO_DATA['crew_roles']
    })


@app.route('/api/crew/multi-reg', methods=['GET'])
def get_multi_reg_crew():
    """Get crew flying on multiple aircraft"""
    return jsonify({
        'count': DEMO_DATA['summary']['multi_reg_count'],
        'crew': DEMO_DATA['multi_reg_crew']
    })


@app.route('/api/utilization', methods=['GET'])
def get_utilization():
    """Get aircraft utilization"""
    return jsonify(DEMO_DATA['utilization'])


@app.route('/api', methods=['GET'])
def api_docs():
    """API Documentation"""
    return jsonify({
        'name': 'Crew Dashboard API',
        'version': '1.0',
        'endpoints': [
            {'method': 'GET', 'path': '/api/dashboard', 'description': 'Get all dashboard data'},
            {'method': 'GET', 'path': '/api/summary', 'description': 'Get summary KPIs'},
            {'method': 'GET', 'path': '/api/aircraft', 'description': 'Get aircraft list'},
            {'method': 'GET', 'path': '/api/crew', 'description': 'Get crew statistics'},
            {'method': 'GET', 'path': '/api/utilization', 'description': 'Get utilization data'}
        ]
    })


# Vercel handler
def handler(request):
    """Vercel serverless function handler"""
    with app.test_client() as client:
        response = client.get(request.path)
        return Response(
            response.data,
            status=response.status_code,
            headers=dict(response.headers)
        )
