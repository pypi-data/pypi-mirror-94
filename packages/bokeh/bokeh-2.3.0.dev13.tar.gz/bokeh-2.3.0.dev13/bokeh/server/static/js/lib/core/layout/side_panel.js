import { Sizeable } from "./types";
import { ContentLayoutable } from "./layoutable";
import { isString } from "../util/types";
// This table lays out the rules for configuring the baseline, alignment, etc. of
// title text, based on it's location and orientation
//
// side    orient        baseline   align     angle   normal-dist
// ------------------------------------------------------------------------------
// above   parallel      bottom     center    0       height
//         normal        middle     left      -90     width
//         horizontal    bottom     center    0       height
//         [angle > 0]   middle     left              width * sin + height * cos
//         [angle < 0]   middle     right             width * sin + height * cos
//
// below   parallel      top        center    0       height
//         normal        middle     right     90      width
//         horizontal    top        center    0       height
//         [angle > 0]   middle     right             width * sin + height * cos
//         [angle < 0]   middle     left              width * sin + height * cos
//
// left    parallel      bottom     center    90      height
//         normal        middle     right     0       width
//         horizontal    middle     right     0       width
//         [angle > 0]   middle     right             width * cos + height * sin
//         [angle < 0]   middle     right             width * cos + height + sin
//
// right   parallel      bottom     center   -90      height
//         normal        middle     left     0        width
//         horizontal    middle     left     0        width
//         [angle > 0]   middle     left              width * cos + height * sin
//         [angle < 0]   middle     left              width * cos + height + sin
const pi2 = Math.PI / 2;
const ALPHABETIC = 'alphabetic';
const HANGING = 'hanging';
const MIDDLE = 'middle';
const LEFT = 'left';
const RIGHT = 'right';
const CENTER = 'center';
const _angle_lookup = {
    above: {
        parallel: 0,
        normal: -pi2,
        horizontal: 0,
        vertical: -pi2,
    },
    below: {
        parallel: 0,
        normal: pi2,
        horizontal: 0,
        vertical: pi2,
    },
    left: {
        parallel: -pi2,
        normal: 0,
        horizontal: 0,
        vertical: -pi2,
    },
    right: {
        parallel: pi2,
        normal: 0,
        horizontal: 0,
        vertical: pi2,
    },
};
const _baseline_lookup = {
    above: {
        parallel: ALPHABETIC,
        normal: MIDDLE,
        horizontal: ALPHABETIC,
        vertical: MIDDLE,
    },
    below: {
        parallel: HANGING,
        normal: MIDDLE,
        horizontal: HANGING,
        vertical: MIDDLE,
    },
    left: {
        parallel: ALPHABETIC,
        normal: MIDDLE,
        horizontal: MIDDLE,
        vertical: ALPHABETIC,
    },
    right: {
        parallel: ALPHABETIC,
        normal: MIDDLE,
        horizontal: MIDDLE,
        vertical: ALPHABETIC,
    },
};
const _align_lookup = {
    above: {
        parallel: CENTER,
        normal: LEFT,
        horizontal: CENTER,
        vertical: LEFT,
    },
    below: {
        parallel: CENTER,
        normal: LEFT,
        horizontal: CENTER,
        vertical: LEFT,
    },
    left: {
        parallel: CENTER,
        normal: RIGHT,
        horizontal: RIGHT,
        vertical: CENTER,
    },
    right: {
        parallel: CENTER,
        normal: LEFT,
        horizontal: LEFT,
        vertical: CENTER,
    },
};
const _align_lookup_negative = {
    above: RIGHT,
    below: LEFT,
    left: RIGHT,
    right: LEFT,
};
const _align_lookup_positive = {
    above: LEFT,
    below: RIGHT,
    left: RIGHT,
    right: LEFT,
};
export class Panel {
    constructor(side) {
        this.side = side;
    }
    get dimension() {
        return this.side == "above" || this.side == "below" ? 0 : 1;
    }
    get normals() {
        switch (this.side) {
            case "above": return [0, -1];
            case "below": return [0, 1];
            case "left": return [-1, 0];
            case "right": return [1, 0];
        }
    }
    get orientation() {
        return this.is_horizontal ? "horizontal" : "vertical";
    }
    get is_horizontal() {
        return this.dimension == 0;
    }
    get is_vertical() {
        return this.dimension == 1;
    }
    get_label_text_heuristics(orient) {
        const { side } = this;
        if (isString(orient)) {
            return {
                baseline: _baseline_lookup[side][orient],
                align: _align_lookup[side][orient],
            };
        }
        else {
            return {
                baseline: "middle",
                align: (orient < 0 ? _align_lookup_negative : _align_lookup_positive)[side],
            };
        }
    }
    get_label_angle_heuristic(orient) {
        if (isString(orient))
            return _angle_lookup[this.side][orient];
        else
            return -orient;
    }
}
Panel.__name__ = "Panel";
export class SideLayout extends ContentLayoutable {
    constructor(panel, get_size, rotate = false) {
        super();
        this.panel = panel;
        this.get_size = get_size;
        this.rotate = rotate;
        if (this.panel.is_horizontal)
            this.set_sizing({ width_policy: "max", height_policy: "fixed" });
        else
            this.set_sizing({ width_policy: "fixed", height_policy: "max" });
    }
    _content_size() {
        const { width, height } = this.get_size();
        if (!this.rotate || this.panel.is_horizontal)
            return new Sizeable({ width, height });
        else
            return new Sizeable({ width: height, height: width });
    }
    has_size_changed() {
        const { width, height } = this._content_size();
        if (this.panel.is_horizontal)
            return this.bbox.height != height;
        else
            return this.bbox.width != width;
    }
}
SideLayout.__name__ = "SideLayout";
//# sourceMappingURL=side_panel.js.map