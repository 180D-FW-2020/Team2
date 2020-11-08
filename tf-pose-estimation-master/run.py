import argparse
import logging
import sys
import time

from tf_pose import common
import cv2
import numpy as np
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

logger = logging.getLogger('TfPoseEstimatorRun')
logger.handlers.clear()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

#overlay = cv2.imread('skeleton.jpg')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tf-pose-estimation run')
    parser.add_argument('--image', type=str, default='./images/p1.jpg')
    parser.add_argument('--model', type=str, default='cmu',
                        help='cmu / mobilenet_thin / mobilenet_v2_large / mobilenet_v2_small')
    parser.add_argument('--resize', type=str, default='0x0',
                        help='if provided, resize images before they are processed. '
                             'default=0x0, Recommends : 432x368 or 656x368 or 1312x736 ')
    parser.add_argument('--resize-out-ratio', type=float, default=4.0,
                        help='if provided, resize heatmaps before they are post-processed. default=1.0')

    args = parser.parse_args()

    w, h = model_wh(args.resize)
    if w == 0 or h == 0:
        e = TfPoseEstimator(get_graph_path(args.model), target_size=(432, 368))
    else:
        e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h))

    # estimate human poses from a single image !
    image = common.read_imgfile(args.image, None, None)
    if image is None:
        logger.error('Image can not be read, path=%s' % args.image)
        sys.exit(-1)

    t = time.time()
    humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=args.resize_out_ratio)
    elapsed = time.time() - t

    logger.info('inference image: %s in %.4f seconds.' % (args.image, elapsed))

    black_background = np.zeros(image.shape)
    skeleton = TfPoseEstimator.draw_humans(black_background, humans, imgcopy=False)
    filename_to_write = args.image.split('/')[-1].split('.')[0] + "_skeleton.jpg"
    print("file", filename_to_write)
    cv2.imwrite(filename_to_write, skeleton)


#image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)

#print("Humans", humans) #list with one element: a string
    human_string = str(humans[0])
    print("Human", human_string)

    keypoints_list = human_string.split('BodyPart:')[1:]

    #'0-(0.52, 0.18) score=0.85 '
    print("List length", len(keypoints_list))
    for joint in keypoints_list:
        #['0-(0.52,', '0.18)', 'score=0.85', ''] we need to get rid of last one
        if len(joint.split(' ')) == '3':
            tuple = joint.split(' ')[:-1]
        else:
            tuple = joint.split(' ')
        index = float((tuple[0]+tuple[1]).split('-')[0])
        xy_coord = (tuple[0]+tuple[1]).split('-')[1]
        score = float(tuple[2].replace('score=',''))
        print("index: ", index, " xy_coord: ", xy_coord, " score: ", score)

    while True:
        cv2.imshow('hi',skeleton)


        k = cv2.waitKey(10)
        # Press q to break
        if k == ord('q'):
            break


'''
    try:
    import matplotlib.pyplot as plt
    print("points", humans)
    fig = plt.figure()
    #        a = fig.add_subplot(2, 2, 1)
    #        a.set_title('Result')
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.show()
    
    
    
    #
    #        bgimg = cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_BGR2RGB)
    #        bgimg = cv2.resize(bgimg, (e.heatMat.shape[1], e.heatMat.shape[0]), interpolation=cv2.INTER_AREA)
    #
    #        # show network output
    #        a = fig.add_subplot(2, 2, 2)
    #        plt.imshow(bgimg, alpha=0.5)
    #        tmp = np.amax(e.heatMat[:, :, :-1], axis=2)
    #        plt.imshow(tmp, cmap=plt.cm.gray, alpha=0.5)
    #        plt.colorbar()
    #/Bv6IK.png
    #        tmp2 = e.pafMat.transpose((2, 0, 1))
    #        tmp2_odd = np.amax(np.absolute(tmp2[::2, :, :]), axis=0)
    #        tmp2_even = np.amax(np.absolute(tmp2[1::2, :, :]), axis=0)
    #
    #        a = fig.add_subplot(2, 2, 3)
    #        a.set_title('Vectormap-x')
    #        # plt.imshow(CocoPose.get_bgimg(inp, target_size=(vectmap.shape[1], vectmap.shape[0])), alpha=0.5)
    #        plt.imshow(tmp2_odd, cmap=plt.cm.gray, alpha=0.5)
    #        plt.colorbar()
    #
    #        a = fig.add_subplot(2, 2, 4)
    #        a.set_title('Vectormap-y')
    #        # plt.imshow(CocoPose.get_bgimg(inp, target_size=(vectmap.shape[1], vectmap.shape[0])), alpha=0.5)
    #        plt.imshow(tmp2_even, cmap=plt.cm.gray, alpha=0.5)
    #        plt.colorbar()
    #        plt.show()
    except Exception as e:
    logger.warning('matplitlib error, %s' % e)
    cv2.imshow('result', image)
    cv2.waitKey()
    '''
