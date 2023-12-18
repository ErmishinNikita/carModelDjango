import tensorflow as tf
from django.http import Http404
from django.shortcuts import render
from djangoProjectMLLab.models import PredictionResult
from PIL import Image, ImageOps
from django.conf import settings
from django.core.files.storage import default_storage
from django.utils.text import slugify
from datetime import datetime
from django.shortcuts import render, redirect
from .models import PredictionResult


classes = ['AVANTE', 'CASPER', 'EV6', 'G70', 'GRANDEUR', 'GV60', 'IONIQ5', 'IONIQ6', 'K5', 'K8', 'K9', 'KONA',
           'Korando', 'Morning', 'NEXO', 'NiroEV', 'PALISADE', 'Ray', 'Rexton', 'SANTAFE', 'SONATA', 'STARIA', 'Seltos',
           'Sorento', 'Sportage', 'Stinger', 'TUCSON', 'Tivoli', 'Torres', 'VENUE', 'qm6', 'sm6', 'xm3']

model = tf.keras.models.load_model('djangoProjectMLLab/cars.h5')


def upload_file(request):
    if request.method == 'POST' and request.FILES:
        uploaded_file = request.FILES['myfile']

        file_name = default_storage.save(f'uploaded_images/{uploaded_file.name}', uploaded_file)
        file_url = default_storage.url(file_name)

        size = (224, 224)
        image = Image.open(uploaded_file)
        image = image.convert("RGB")
        image = ImageOps.fit(image, size, Image.LANCZOS)
        img_array = tf.keras.preprocessing.image.img_to_array(image)
        img_array = tf.expand_dims(img_array, 0)

        predictions = model.predict(img_array).flatten()
        predictions = tf.where(predictions < 0.5, 0, 1)
        predicted_class_index = tf.argmax(predictions)

        predicted_class = classes[predicted_class_index]

        # Сохраняем результат в базе данных
        prediction_result = PredictionResult.objects.create(
            file_name=uploaded_file.name,
            file_path=file_url,
            result=predicted_class,
            prediction_datetime=datetime.now()
        )

        res_message = f'Скорее всего на этом фото {predicted_class}'

        return render(request, 'upload_file.html', {
            'res_message': res_message,
        })
    return render(request, 'upload_file.html')


def show_results(request):
    predictions = PredictionResult.objects.all()
    return render(request, 'show_results.html', {'predictions': predictions})

def delete_prediction(request, prediction_id):
    try:
        prediction = PredictionResult.objects.get(pk=prediction_id)
        prediction.delete()
        return redirect('show_results')
    except PredictionResult.DoesNotExist:
        raise Http404("PredictionResult does not exist")