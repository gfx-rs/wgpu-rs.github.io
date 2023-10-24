var srcIndex = JSON.parse('{\
"player":["",[],["lib.rs"]],\
"wgpu":["",[["backend",[],["direct.rs","mod.rs"]],["util",[],["belt.rs","device.rs","encoder.rs","indirect.rs","init.rs","mod.rs"]]],["context.rs","lib.rs","macros.rs"]],\
"wgpu_core":["",[["command",[],["bind.rs","bundle.rs","clear.rs","compute.rs","draw.rs","memory_init.rs","mod.rs","query.rs","render.rs","transfer.rs"]],["device",[],["global.rs","life.rs","mod.rs","queue.rs","resource.rs","trace.rs"]],["init_tracker",[],["buffer.rs","mod.rs","texture.rs"]],["track",[],["buffer.rs","metadata.rs","mod.rs","range.rs","stateless.rs","texture.rs"]]],["binding_model.rs","conv.rs","error.rs","global.rs","hal_api.rs","hub.rs","id.rs","identity.rs","instance.rs","lib.rs","pipeline.rs","present.rs","registry.rs","resource.rs","storage.rs","validation.rs"]],\
"wgpu_example":["",[],["framework.rs","lib.rs","utils.rs"]],\
"wgpu_hal":["",[["auxil",[],["mod.rs","renderdoc.rs"]],["gles",[],["adapter.rs","command.rs","conv.rs","device.rs","egl.rs","mod.rs","queue.rs"]],["vulkan",[],["adapter.rs","command.rs","conv.rs","device.rs","instance.rs","mod.rs"]]],["empty.rs","lib.rs"]],\
"wgpu_macros":["",[],["lib.rs"]],\
"wgpu_test":["",[],["config.rs","image.rs","init.rs","isolation.rs","lib.rs","native.rs","params.rs","report.rs","run.rs"]],\
"wgpu_types":["",[],["assertions.rs","lib.rs","math.rs"]]\
}');
createSrcSidebar();
