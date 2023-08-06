import cv2
import multiprocessing as mp
from monkey_vision.app.utils.group_points import group_coordinates
from monkey_vision.app import vision_points, vision_compare
# from dev import dev as DEV

# imageURI = "assets/test_image.png"
# imageURICompare = "assets/test_image_popup.png"


def get_event_points(imageURI, isDev=False):
    if imageURI is None:
        return
    # if isDev:
    #     image = DEV.get_image(imageURI)
    #     DEV.draw_text_areas(imageURI, image)
    #     DEV.draw_paragraphs(imageURI, image)
        # DEV.draw_convexHulls(imageURI, image)
    # array containing the generated screen points from the image analysis
    event_points = vision_points.get_vision_points(imageURI)
    # Group closest points together based on proximity.
    groups = group_coordinates(event_points)
    # if isDev:
    #     DEV.draw_grouped_event_points(groups, image)
    #     DEV.show_image(image)
    return groups


def percengate_compare(*args):
    """
    Method to calculate the percentage match of a provided array of images. 
    Will run parallely the percentage compare and return the results.
    args[0] base image path. To be matched with all the rest of the provided image paths.
    @returns array of percentage matches
    """
    if args[0] is None or args[1] is None:
        return
    pool = mp.Pool(mp.cpu_count())
    results = [pool.apply(vision_compare.get_percentage_match, args=(args[0], item)) for item in args[1:]]
    pool.close()   
    return results
