import os
import sys
import json
import logging
from collections import defaultdict

from vispy import scene
from vispy.scene.visuals import Text
from vispy import app
import numpy as np

import pandas as pd

from imageio import imread

import click

from skimage.draw import circle

logger = logging.getLogger(__file__)

canvas = scene.SceneCanvas(keys='interactive')
canvas.size = 800, 600
canvas.show()

# Set up a viewbox to display the image with interactive pan/zoom
view = canvas.central_widget.add_view()


palettes = {
    '1': [0, 255, 0],
    '2': [255, 0, 0]
}


def label_coords_dict_to_dataframe(label_coords_dict):
    print(label_coords_dict)


def load_points(points_fpath):

    name, ext = os.path.splitext(points_fpath)

    if ext == ".csv":
        df = pd.read_csv(points_fpath)
        points = {'1': [(p.X, p.Y) for p in df.itertuples()]}
        return points

    if ext == ".json":
        with open(points_fpath) as fh:
            points = json.load(fh)
        return points

    raise ValueError(f"Unknown points file format: {ext}")


def save_points(points, output_fpath):

    logger.info(f"Saving {points}")

    name, ext = os.path.splitext(output_fpath)
    # with open(output_fpath, 'w') as fh:
    #     json.dump(points, fh)
    # print(points)
    # df = pd.DataFrame(points, columns=['X', 'Y'])
    # df.to_csv(output_fpath, index=False)
    if ext == ".csv":
        df = pd.DataFrame(points['1'], columns=['X', 'Y'])
        df.to_csv(output_fpath, index=False)
        return

    if ext == ".json":
        with open(output_fpath, 'w') as fh:
            json.dump(points, fh)
        return

    raise ValueError(f"Unknown points file format: {ext}")


def coerce_to_rgb(im):

    ndim = len(im.shape)

    if ndim == 3:
        return im
    if ndim == 2:
        return np.dstack(3 * [im])

    raise ValueError("Can't handle image")

@click.command()
@click.argument('image_fpath')
@click.argument('input_points_fpath')
@click.argument('output_points_fpath', required=False)
def main(image_fpath, input_points_fpath, output_points_fpath):
    global canvas

    logging.basicConfig(level=logging.INFO)

    im = imread(image_fpath)
    logger.info(f"Loaded image with shape {im.shape}")
    im = coerce_to_rgb(im)
    image = scene.visuals.Image(im, parent=view.scene)

    app.current_pos = None

    if output_points_fpath:
        points = load_points(input_points_fpath)
        # with open(input_points_fpath) as fh:
        #     points = json.load(fh)
        output_fpath = output_points_fpath
    else:
        points = defaultdict(list)
        output_fpath = input_points_fpath
    
    print(points)

    @canvas.events.mouse_press.connect
    def on_mouse_press(event):
        # print("Press pos:", event.pos)
        # get transform mapping from canvas to image
        tr = view.node_transform(image)
        # print("Image pos:", tr.map(event.pos)[:2])
        x, y = tr.map(event.pos)[:2]

        print("Click at ", x, y)

        # c, r = int(x), int(y)

        # points.append(np.array((r, c)))

        # rr, cc = circle(r, c, 5)
        # im[rr, cc] = 255, 0, 0
        # image.set_data(im)
        # canvas.update()

    @canvas.connect
    def on_mouse_move(event):
        app.current_pos = event.pos

    def update_drawing():
        draw_im = im.copy()
        for label, point_coords in points.items():
            for r, c in point_coords:
                rr, cc = circle(r, c, 3)
                try:
                    draw_im[rr, cc] = palettes[label]
                except IndexError:
                    print(f"Point at {r}, {c} out of bounds")
                    raise
            
        image.set_data(draw_im)
        canvas.update()

    @canvas.events.key_press.connect
    def key_event(event):

        mark_keys = palettes.keys()

        if event.key.name == 'Escape':
            app.quit()

        if event.key.name in mark_keys:
            tr = view.node_transform(image)
            x, y = tr.map(app.current_pos)[:2]
            c, r = int(x), int(y)
            print(f"Mark {event.key.name} at ({r},{c})")
            points[event.key.name].append((r, c))
            update_drawing()

        # if event.key.name == 'P':
        #     print("Added point")
        #     tr = view.node_transform(image)
        #     x, y = tr.map(app.current_pos)[:2]
        #     c, r = int(x), int(y)
        #     points.append(np.array((r, c)))
        #     update_drawing()

        if event.key.name == 'D':
            plist = points['1']
            tr = view.node_transform(image)
            x, y = tr.map(app.current_pos)[:2]
            c, r = int(x), int(y)
            deltas = np.array(plist) - np.array((r, c))
            sq_dists = np.sum(deltas * deltas, axis=1)
            del plist[np.argmin(sq_dists)]
            update_drawing()

        if event.key.name == 'S':
            save_points(points, output_fpath)
            # with open(output_fpath, 'w') as fh:
            #     json.dump(points, fh)
            # print(points)
            # df = pd.DataFrame(points, columns=['X', 'Y'])
            # df.to_csv(output_fpath, index=False)

    # t1 = scene.visuals.Text('Text in root scene (24 pt)', parent=image, color='red', pos=(100,100))
    # t1.font_size = 24
    # Set 2D camera (the camera will scale to the contents in the scene)
    view.camera = scene.PanZoomCamera(aspect=1)
    view.camera.set_range()
    view.camera.flip = (False, True, False)

    update_drawing()

    app.run()


if __name__ == '__main__':
    main()
