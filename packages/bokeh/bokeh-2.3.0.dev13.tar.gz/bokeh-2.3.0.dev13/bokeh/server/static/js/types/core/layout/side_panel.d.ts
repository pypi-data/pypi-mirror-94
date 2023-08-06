import { Size, Sizeable } from "./types";
import { ContentLayoutable } from "./layoutable";
import { Side, Orientation } from "../enums";
export declare type Orient = "parallel" | "normal" | "horizontal" | "vertical";
export declare class Panel {
    readonly side: Side;
    constructor(side: Side);
    get dimension(): 0 | 1;
    get normals(): [number, number];
    get orientation(): Orientation;
    get is_horizontal(): boolean;
    get is_vertical(): boolean;
    get_label_text_heuristics(orient: Orient | number): {
        baseline: CanvasTextBaseline;
        align: CanvasTextAlign;
    };
    get_label_angle_heuristic(orient: Orient | number): number;
}
export declare class SideLayout extends ContentLayoutable {
    readonly panel: Panel;
    readonly get_size: () => Size;
    readonly rotate: boolean;
    constructor(panel: Panel, get_size: () => Size, rotate?: boolean);
    protected _content_size(): Sizeable;
    has_size_changed(): boolean;
}
//# sourceMappingURL=side_panel.d.ts.map