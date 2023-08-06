import numpy as np
import sys, os

class accuracy_boxes():
    def __init__(self, boxes):
        """
        Format boxes: [box1, box2, box3]
        Format box: [xmin, ymin, xmax, ymax, label_name, id_job]
        """
        self.boxes = boxes
        self.label_names = [i[4] for i in boxes]

    def IOU(self,bbox1, bbox2):
        # bbox[xmin, ymin, xmax, ymax]
        assert bbox1[0] < bbox1[2]
        assert bbox1[1] < bbox1[3]
        assert bbox2[0] < bbox2[2]
        assert bbox2[1] < bbox2[3]

        x_left = max(bbox1[0],bbox2[0])
        y_top = max(bbox1[1],bbox2[1])
        x_right = min(bbox1[2],bbox2[2])
        y_bottom = min(bbox1[3], bbox2[3])

        if x_right < x_left or y_bottom < y_top:
            return 0.0

        intersection_area = (x_right - x_left) * (y_bottom - y_top)

        bbox1_area = (bbox1[2]-bbox1[0])*(bbox1[3]-bbox1[1])
        bbox2_area = (bbox2[2]-bbox2[0])*(bbox2[3]-bbox2[1])

        iou = intersection_area *100 / float(bbox1_area + bbox2_area - intersection_area)

        return round(iou,2) 

    def check_labels(self, label_names):
        set_label = list(set(label_names))
        count = 0
        for label in set_label:
            if label_names.count(label) > count:
                label_name = [label]
                count = label_names.count(label)
            elif label_names.count(label) == count:
                label_name.append(label)
        if len(label_name) > 1:
            raise NameError("Admin check label name", label_name)
        else:
            return label_name[0]


    def verify_boxes(self):
        box_true = {'boxes': [], 'iou': 0}
        for box in self.boxes:
            _box_check = []
            iou_check = 0
            for box_iou in self.boxes:
                if box != box_iou:
                    iou = self.IOU(box, box_iou)
                    if iou > 70:
                        _box_check.append(box_iou)
                        iou_check += iou
            if _box_check != 0 and iou_check > box_true['iou']:
                _box_check.append(box)
                box_true['boxes'] = _box_check.copy()
                box_true['iou']
        
        try:
            #Calculate avg boxes and accuracy box with label_name
            label_name = self.check_labels(self.label_names)
            val_box = [0,0,0,0]
            for box in box_true['boxes']:
                if box[4] == label_name:
                    val_box = np.add(val_box,box[:4])

            box_avg = (val_box//self.label_names.count(label_name)).tolist()
            result_acc = {
                'label_name': label_name,
                'accuracy_box': {},
                'true_box': box_avg
            }
            for box in box_true['boxes']:
                if box[4] == label_name:
                    accuracy = self.IOU(box_avg, box[:4])
                    result_acc['accuracy_box'].update({
                        str(box[5]) : accuracy
                    })
                else:
                    result_acc['accuracy_box'].update({
                        str(box[5]) : 0
                    })
            return result_acc
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return None
