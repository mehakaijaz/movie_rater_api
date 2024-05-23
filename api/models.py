from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
# from django.db.models import Avg


class Movie(models.Model):
    title=models.CharField(max_length=50)
    description=models.TextField(max_length=500)
    
    def no_of_ratings(self):
        return Rating.objects.filter(movie=self).count()
    
    def avg_rating(self):
        total = 0
        ratings = Rating.objects.filter(movie=self)
        for rating in ratings:
            total += rating.stars
        if len(ratings) > 0:
            return total/len(ratings)
        else:
            return 
    
    # Alternatively, using aggregation
    # def avg_rating(self):
    #     return Rating.objects.filter(movie=self).aggregate(average=Avg('stars'))['average']

    def __str__(self):
        return self.title

class Rating(models.Model):
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE,null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    stars=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    
    class Meta:
        unique_together = (('user', 'movie'),)
        index_together = (('user', 'movie'),)
        # The class Meta block with unique_together and index_together helps 
        # enforce data integrity and optimize query performance for composite fields
    
    def __str__(self):
        return f"{self.movie.title} - {self.user.username}"