/*
Copyright 2020 Lucas Heitzmann Gabrielli.
This file is part of gdstk, distributed under the terms of the
Boost Software License - Version 1.0.  See the accompanying
LICENSE file or <http://www.boost.org/LICENSE_1_0.txt>
*/

#ifndef GDSTK_HEADER_CELL
#define GDSTK_HEADER_CELL

#define __STDC_FORMAT_MACROS
#define _USE_MATH_DEFINES

#include <stdint.h>
#include <stdio.h>
#include <time.h>

#include "array.h"
#include "flexpath.h"
#include "label.h"
#include "map.h"
#include "polygon.h"
#include "reference.h"
#include "robustpath.h"
#include "style.h"

namespace gdstk {

// enum struct FilterOperation { And, Or, XOr, NAnd, NOr, NXOr };

struct Cell {
    char* name;
    Array<Polygon*> polygon_array;
    Array<Reference*> reference_array;
    Array<FlexPath*> flexpath_array;
    Array<RobustPath*> robustpath_array;
    Array<Label*> label_array;
    Property* properties;
    // Used by the python interface to store the associated PyObject* (if any).
    // No functions in gdstk namespace should touch this value!
    void* owner;

    void print(bool all) const;

    void clear();

    void bounding_box(Vec2& min, Vec2& max) const;

    void copy_from(const Cell& cell, const char* new_name, bool deep_copy);

    void get_polygons(bool apply_repetitions, bool include_paths, int64_t depth,
                      Array<Polygon*>& result) const;
    void get_flexpaths(bool apply_repetitions, int64_t depth, Array<FlexPath*>& result) const;
    void get_robustpaths(bool apply_repetitions, int64_t depth, Array<RobustPath*>& result) const;
    void get_labels(bool apply_repetitions, int64_t depth, Array<Label*>& result) const;

    void get_dependencies(bool recursive, Map<Cell*>& result) const;
    void get_raw_dependencies(bool recursive, Map<RawCell*>& result) const;

    // Return removed references
    void flatten(bool apply_repetitions, Array<Reference*>& removed_references);

    // TODO: https://github.com/heitzmann/gdstk/issues/23
    //
    // Better idea: implement only the Python version for efficiency. In C++ there should be a
    // tutorial recipe.
    //
    // Remove element if: layers.contain(element.layer) operation _types.contain(elements._type)
    // Paths can have individual elements removed as necessary.  Return removed elements.
    // void remove_elements(const Array<uint32_t> layers, const Array<uint32_t> datatypes,
    //                      FilterOperation operation, Array<Polygon*>& removed_polygons,
    //                      Array<FlexPath*>& removed_flexpaths,
    //                      Array<RobustPath*>& removed_robustpaths);
    // void remove_elements(const Array<uint32_t> layers, const Array<uint32_t> texttypes,
    //                      FilterOperation operation, Array<Label*>& removed_labels);

    void to_gds(FILE* out, double scaling, uint64_t max_points, double precision,
                const tm* timestamp) const;

    void to_svg(FILE* out, double scaling, const char* attributes) const;

    void write_svg(const char* filename, double scaling, StyleMap& style, StyleMap& label_style,
                   const char* background, double pad, bool pad_as_percentage) const;
};

}  // namespace gdstk

#endif
