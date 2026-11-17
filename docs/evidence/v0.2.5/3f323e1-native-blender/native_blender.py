import hashlib
import json
import sys
import traceback
from pathlib import Path

import bpy
from mathutils import Vector

OUT = Path(r'C:\Evidence\verification-output')
OUT.mkdir(parents=True, exist_ok=True)
REPORT = {'candidate_sha': '3f323e1ed8c38a44affb432420f6428bb6d57677',
          'host': bpy.app.version_string, 'background': bpy.app.background,
          'method': 'Scripted operators in a real Blender GUI inside offline Windows Sandbox',
          'gui_visual_inspection': 'NOT_EXECUTED', 'extension_manager_install': 'NOT_EXECUTED',
          'ae_execution': 'NOT_EXECUTED', 'results': {}, 'packages': []}

def write_report():
    (OUT / 'native-blender.json').write_text(json.dumps(REPORT, indent=2), encoding='utf-8')

def run():
    try:
        assert not bpy.app.background, 'This campaign requires the native GUI event loop'
        sys.path.insert(0, r'C:\Inputs\scripts\addons')
        import addon_utils
        addon_utils.enable('cutbridge', default_set=True, persistent=True)
        import cutbridge
        from cutbridge.operators import _all_validation_issues
        from cutbridge import core, update_ops
        assert cutbridge.version.__version__ == '0.2.5'
        assert hasattr(bpy.types.Scene, 'cutbridge')
        assert not bpy.app.timers.is_registered(update_ops._startup_update_check)
        REPORT['results']['exact_candidate_enable'] = 'PASS'
        REPORT['results']['startup_scheduler_disabled'] = 'PASS'
        areas = [area for window in bpy.context.window_manager.windows for area in window.screen.areas if area.type == 'VIEW_3D']
        assert areas
        for area in areas:
            area.spaces.active.show_region_ui = True
            area.tag_redraw()
        REPORT['sidebar_open'] = True
        REPORT['cutbridge_tab_visually_confirmed'] = False

        scene = bpy.context.scene
        scene.render.engine = 'BLENDER_EEVEE'
        scene.render.resolution_x = 320
        scene.render.resolution_y = 180
        scene.render.resolution_percentage = 100
        scene.render.fps = 24
        scene.frame_start, scene.frame_end = 1, 3
        if hasattr(scene.render, 'compositor_device'):
            scene.render.compositor_device = 'CPU'
        camera = scene.camera
        camera.location = (7, -7, 5)
        camera.rotation_euler = (Vector((0, 0, 0)) - camera.location).to_track_quat('-Z', 'Y').to_euler()
        cube = bpy.data.objects.get('Cube')
        assert cube is not None
        bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, -1))
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
        marker = bpy.context.object
        marker.name = 'Native025Null'
        marker['cutbridge_handoff_3d'] = True

        scene.render.use_freestyle = True
        layer = bpy.context.view_layer
        layer.use_freestyle = True
        layer.freestyle_settings.as_render_pass = True
        layer.use_pass_shadow = True
        layer.use_pass_z = True
        artist_tree = bpy.data.node_groups.new('ArtistCompositor025', 'CompositorNodeTree')
        artist_node = artist_tree.nodes.new('CompositorNodeRGB')
        artist_node.label = 'Artist node must survive'
        scene.compositing_node_group = artist_tree
        settings = scene.cutbridge
        settings.language = 'EN'
        settings.project, settings.episode, settings.scene_id = 'Native025', 'EP01', 'SC010'
        settings.cut, settings.take = 'C001', 'T01'
        settings.output_dir = str(OUT / '\u30d1\u30c3\u30b1\u30fc\u30b8')
        settings.studio_preset_mode = 'MANUAL'
        settings.pass_beauty = settings.pass_line = settings.pass_shadow = settings.pass_depth = True
        settings.per_pass_formats_enabled = True
        settings.format_beauty = settings.format_line = settings.format_shadow = 'PNG'
        settings.format_depth = 'OPEN_EXR'
        settings.handoff_3d_enabled = True

        for version in (1, 2, 3):
            settings.version = version
            for frame in (1, 3):
                cube.location.x = version * 0.15 + frame * 0.1
                cube.keyframe_insert(data_path='location', frame=frame)
                marker.location.x = version * 0.25 + frame * 0.15
                marker.keyframe_insert(data_path='location', frame=frame)
                camera.location.x = 7 + version * 0.1 + frame * 0.05
                camera.keyframe_insert(data_path='location', frame=frame)
            scene.frame_set(1)
            bpy.ops.wm.save_as_mainfile(filepath=str(OUT / f'native025-V{version:03d}.blend'))
            issues = _all_validation_issues(bpy.context, for_build=True)
            assert not [issue for issue in issues if issue['level'] == 'ERROR'], issues
            assert bpy.ops.cutbridge.validate() == {'FINISHED'}
            assert bpy.ops.cutbridge.build_package() == {'FINISHED'}
            root = Path(settings.last_package_path)
            manifest = json.loads((root / 'cutbridge.json').read_text())
            assert manifest['handoff_3d']
            assert artist_node in artist_tree.nodes.values()
            bpy.ops.render.render(animation=True)
            payload = sorted(path for path in root.rglob('*') if path.suffix.lower() in ('.png', '.exr'))
            assert len(payload) == 12 and all(path.stat().st_size > 0 for path in payload), [(str(p), p.stat().st_size) for p in payload]
            before = {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in payload}
            blocked = False
            try:
                blocked = bpy.ops.cutbridge.build_package() == {'CANCELLED'}
            except RuntimeError:
                blocked = True
            assert blocked, 'Same-version rendered package replacement was not blocked'
            assert before == {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in payload}
            assert artist_node in artist_tree.nodes.values()
            REPORT['packages'].append({'version': version, 'root': str(root), 'outputs': len(payload),
                                       'manifest_sha256': hashlib.sha256((root / 'cutbridge.json').read_bytes()).hexdigest(),
                                       'same_version_payload_preserved': True})
            write_report()

        prior_settings = (settings.project, settings.episode, settings.scene_id, settings.cut, settings.take, settings.version)
        settings.language = 'JA'
        assert prior_settings == (settings.project, settings.episode, settings.scene_id, settings.cut, settings.take, settings.version)
        settings.language = 'EN'
        REPORT['results'].update(native_validate_and_build='PASS', real_four_pass_render='PASS',
                                 mixed_png_exr='PASS', camera_empty_producer='PASS',
                                 versions_v001_v002_v003='PASS', same_version_overwrite_block='PASS',
                                 artist_node_preservation='PASS', locale_identity_preservation='PASS')
        REPORT['overall_scope_result'] = 'PASS'
        REPORT['fixture_sha256'] = hashlib.sha256((OUT / 'native025-V001.blend').read_bytes()).hexdigest()
        bpy.ops.wm.save_as_mainfile(filepath=str(OUT / 'native025-V003.blend'))
    except Exception:
        REPORT['overall_scope_result'] = 'FAIL'
        REPORT['error'] = traceback.format_exc()
    finally:
        write_report()
        bpy.ops.wm.quit_blender()
    return None

write_report()
bpy.app.timers.register(run, first_interval=2.0)
