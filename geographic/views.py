from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import Region, TrendingMovie, UserRegion
from .services import TrendingCalculator, RegionService

class TrendingMapView(View):
    """View for the trending movies map page"""
    
    @method_decorator(login_required)
    def get(self, request):
        regions = Region.objects.filter(is_active=True)
        context = {
            'regions': regions,
        }
        return render(request, 'geographic/trending_map.html', context)

@login_required
def trending_data_api(request):
    """API endpoint to get trending movies data for all regions"""
    try:
        calculator = TrendingCalculator()
        trending_data = calculator.calculate_trending_for_all_regions()
        
        # Format data for frontend
        formatted_data = {}
        for region_id, data in trending_data.items():
            region = data['region']
            formatted_data[region_id] = {
                'region': {
                    'id': region.id,
                    'name': region.name,
                    'code': region.code,
                    'latitude': region.latitude,
                    'longitude': region.longitude,
                    'population': region.population
                },
                'trending_movies': [
                    {
                        'id': movie_data['movie'].id,
                        'name': movie_data['movie'].name,
                        'price': movie_data['movie'].price,
                        'image': movie_data['movie'].image.url if movie_data['movie'].image else None,
                        'purchase_count': movie_data['purchase_count'],
                        'trending_score': movie_data['trending_score']
                    }
                    for movie_data in data['trending_movies']
                ]
            }
        
        return JsonResponse({
            'success': True,
            'data': formatted_data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
def region_trending_api(request, region_id):
    """API endpoint to get trending movies for a specific region"""
    try:
        calculator = TrendingCalculator()
        trending_movies = calculator.calculate_trending_for_region(region_id)
        
        formatted_movies = [
            {
                'id': movie_data['movie'].id,
                'name': movie_data['movie'].name,
                'price': movie_data['movie'].price,
                'description': movie_data['movie'].description,
                'image': movie_data['movie'].image.url if movie_data['movie'].image else None,
                'purchase_count': movie_data['purchase_count'],
                'total_quantity': movie_data['total_quantity'],
                'trending_score': movie_data['trending_score']
            }
            for movie_data in trending_movies
        ]
        
        return JsonResponse({
            'success': True,
            'data': formatted_movies
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def set_user_region_api(request):
    """API endpoint to set user's region"""
    try:
        data = json.loads(request.body)
        region_id = data.get('region_id')
        
        if not region_id:
            return JsonResponse({
                'success': False,
                'error': 'Region ID is required'
            }, status=400)
        
        region = Region.objects.get(id=region_id)
        RegionService.set_user_region(request.user, region)
        
        return JsonResponse({
            'success': True,
            'message': f'Region set to {region.name}'
        })
    except Region.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Region not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
def user_region_api(request):
    """API endpoint to get user's current region"""
    try:
        region = RegionService.get_user_region(request.user)
        if region:
            return JsonResponse({
                'success': True,
                'data': {
                    'id': region.id,
                    'name': region.name,
                    'code': region.code,
                    'latitude': region.latitude,
                    'longitude': region.longitude
                }
            })
        else:
            return JsonResponse({
                'success': True,
                'data': None
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)