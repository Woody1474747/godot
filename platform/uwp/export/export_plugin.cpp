/**************************************************************************/
/*  export_plugin.cpp                                                     */
/**************************************************************************/
/*                         This file is part of:                          */
/*                             GODOT ENGINE                               */
/*                        https://godotengine.org                         */
/**************************************************************************/
/* Copyright (c) 2014-present Godot Engine contributors (see AUTHORS.md). */
/* Copyright (c) 2007-2014 Juan Linietsky, Ariel Manzur.                  */
/*                                                                        */
/* Permission is hereby granted, free of charge, to any person obtaining  */
/* a copy of this software and associated documentation files (the        */
/* "Software"), to deal in the Software without restriction, including    */
/* without limitation the rights to use, copy, modify, merge, publish,    */
/* distribute, sublicense, and/or sell copies of the Software, and to     */
/* permit persons to whom the Software is furnished to do so, subject to  */
/* the following conditions:                                              */
/*                                                                        */
/* The above copyright notice and this permission notice shall be         */
/* included in all copies or substantial portions of the Software.        */
/*                                                                        */
/* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,        */
/* EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF     */
/* MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. */
/* IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY   */
/* CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,   */
/* TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE      */
/* SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.                 */
/**************************************************************************/

#include "export_plugin.h"

#include "editor/export/editor_export.h"

#include "core/io/image.h"
#include "core/templates/packed_array.h"
#include "main/app_icon_uwp.gen.h"
#include "scene/resources/image_texture.h"

#include <cstring>

EditorExportPlatformUWP::EditorExportPlatformUWP() {
        set_name("Universal Windows Platform");
        set_os_name("UWP");

        Ref<Image> default_icon;
        default_icon.instantiate();

        PackedByteArray icon_data;
        icon_data.resize(sizeof(app_icon_uwp_png));
        if (icon_data.size() == sizeof(app_icon_uwp_png)) {
                std::memcpy(icon_data.ptrw(), app_icon_uwp_png, sizeof(app_icon_uwp_png));
                if (default_icon->load_png_from_buffer(icon_data) == OK) {
                        set_logo(ImageTexture::create_from_image(default_icon));
                }
        }
}

String EditorExportPlatformUWP::get_template_file_name(const String &p_target, const String &p_arch) const {
        return "uwp_" + p_target + "_" + p_arch + ".exe";
}

List<String> EditorExportPlatformUWP::get_binary_extensions(const Ref<EditorExportPreset> &p_preset) const {
        List<String> list;
        list.push_back("exe");
        list.push_back("zip");
        return list;
}
