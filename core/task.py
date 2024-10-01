from celery import shared_task
from django.utils import timezone
from pujo.models import Pujo, LastScoreModel

@shared_task
def update_pujo_scores():
    current_time = timezone.now()
    # Adjust X to the desired number of hours
    X = 6  

    pujos = Pujo.objects.filter(updated_at__lt=current_time - timezone.timedelta(hours=X))
    for pujo in pujos:
        # Sum all positive last scores in the last 2X hours
        last_scores = LastScoreModel.objects.filter(
            pujo=pujo,
            last_updated_at__gt=current_time - timezone.timedelta(hours=2 * X),
            value__gt=0
        )

        # sum all positive scores
        score_sum = sum(score.value for score in last_scores if score.value > 0)

        # Update the pujo's score
        pujo.search_score -= score_sum
        pujo.save()

        # Remove all previous last scores
        last_scores.delete()

        # Log the score summation - the new score
        LastScoreModel.objects.create(pujo=pujo, value=-score_sum)

