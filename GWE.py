bl_info = {
    "name": "Game Workflow Exporter",
    "blender": (2, 90, 0),
    "category": "Import-Export",
}

import bpy
from bpy.props import (BoolProperty, IntProperty, StringProperty, PointerProperty, EnumProperty)
from bpy.app.handlers import persistent

# ------------------------------------------------------------------------
#    Handlers
# ------------------------------------------------------------------------
#presave
@persistent
def GWE_SaveHandler(dummy):
    if bpy.data.objects.get('.GWE_EmptySerializer') is None:
        print('GWE: Creating Empty for Serialization')
        bpy.ops.scene.new(type='EMPTY')
        obj = bpy.data.objects.new('.GWE_EmptySerializer', None)
        obj.use_fake_user = True
        bpy.ops.scene.delete()

    obj = bpy.data.objects.get('.GWE_EmptySerializer')

    mytool = bpy.context.window_manager.GWE_tool
    myserializer = obj.GWE_serializer

    myserializer.GWE_ExportName = mytool.GWE_ExportName
    myserializer.GWE_ExportPath = mytool.GWE_ExportPath
    myserializer.GWE_ExportType = mytool.GWE_ExportType
    myserializer.GWE_ExportTypeAnimationFake = mytool.GWE_ExportTypeAnimationFake    
    
    myserializer.GWE_ControlRigPointer = mytool.GWE_ControlRigPointer
    myserializer.GWE_MeshPointer = mytool.GWE_MeshPointer
    myserializer.GWE_DeformationRigPointer = mytool.GWE_DeformationRigPointer
    myserializer.GWE_bRigGenerated = mytool.GWE_bRigGenerated
    
    myserializer.GWE_AnimLinkedSkeletonFilePath = mytool.GWE_AnimLinkedSkeletonFilePath
    myserializer.GWE_AnimLinkedSkeletonCollection = mytool.GWE_AnimLinkedSkeletonCollection
    myserializer.GWE_bAnimLinked = mytool.GWE_bAnimLinked
    
    myserializer.GWE_ControlRigName = mytool.GWE_ControlRigName
    myserializer.GWE_DeformationRigName = mytool.GWE_DeformationRigName
    myserializer.GWE_MeshName = mytool.GWE_MeshName
    
    mserializer.GWE_NumberOfAnimations = mytool.GWE_NumberOfAnimations

#postload
@persistent
def GWE_LoadHandler(dummy):
    #If we have an EmptySerializer, update our window manager's properties to match our object's
    if bpy.data.objects.get('.GWE_EmptySerializer') is not None:
        obj = bpy.data.objects.get('.GWE_EmptySerializer')

        mytool = bpy.context.window_manager.GWE_tool
        myserializer = obj.GWE_serializer

        mytool.GWE_ExportName = myserializer.GWE_ExportName
        mytool.GWE_ExportPath = myserializer.GWE_ExportPath
        mytool.GWE_ExportType = myserializer.GWE_ExportType
        mytool.GWE_ExportTypeAnimationFake = myserializer.GWE_ExportTypeAnimationFake    
        
        mytool.GWE_ControlRigPointer = myserializer.GWE_ControlRigPointer
        mytool.GWE_MeshPointer = myserializer.GWE_MeshPointer
        mytool.GWE_DeformationRigPointer = myserializer.GWE_DeformationRigPointer
        mytool.GWE_bRigGenerated = myserializer.GWE_bRigGenerated
        
        mytool.GWE_AnimLinkedSkeletonFilePath = myserializer.GWE_AnimLinkedSkeletonFilePath
        mytool.GWE_AnimLinkedSkeletonCollection = myserializer.GWE_AnimLinkedSkeletonCollection
        mytool.GWE_bAnimLinked = myserializer.GWE_bAnimLinked
        
        mytool.GWE_ControlRigName = myserializer.GWE_ControlRigName
        mytool.GWE_DeformationRigName = myserializer.GWE_DeformationRigName
        mytool.GWE_MeshName = myserializer.GWE_MeshName
        
        mytool.GWE_NumberOfAnimations = myserializer.GWE_NumberOfAnimations
        



# ------------------------------------------------------------------------
#    Serialized Properties
# ------------------------------------------------------------------------
class GWE_Properties(bpy.types.PropertyGroup):

    GWE_ExportName: StringProperty(
        name="Name",
        description="Choose a name for this/these object(s)",
        default="",
        maxlen=1024,
        )

    GWE_ExportPath: StringProperty(
        name = "Path",
        description="Choose where you would like to save this/these object(s)",
        default="",
        maxlen=1024,
        subtype='DIR_PATH'
        )
        
    GWE_ExportType: EnumProperty(
        name='Type',
        description='What type of asset is this?',
        items = [('0','None',''), 
                ('1','Mesh',''),
                ('2','Skeleton','')],
        default='0'
        )
        
    GWE_ExportTypeAnimationFake: EnumProperty(
        name='Type',
        description='What type of asset is this?',
        items = [('0', 'Not Animation', ''),
                ('1', 'Unlinked Animation', ''),
                ('2', 'Animation', '')],
        default='0'
    )
    
    GWE_ControlRigPointer: PointerProperty(
        name='Control Rig',
        type=bpy.types.Object
        )
    
    GWE_MeshPointer: PointerProperty(
        name='Mesh',
        type=bpy.types.Object
        )
        
    GWE_DeformationRigPointer: PointerProperty(
        name='Deformation Rig',
        type=bpy.types.Object
        )
        
    GWE_bRigGenerated: BoolProperty(
        default=False
        )
                
    GWE_AnimLinkedSkeletonFilePath: StringProperty(
        name='Skeleton File Path',
        subtype='DIR_PATH'
        )
        
    GWE_AnimLinkedSkeletonCollection: StringProperty(
        name='Skeleton Collection'
    )
    
    GWE_bAnimLinked: BoolProperty(
        default=False
    )
    
    GWE_ControlRigName: StringProperty(
        name='Control Rig Name'
    )
    
    GWE_DeformationRigName: StringProperty(
        name='Deformation Rig Name'
    )

    GWE_MeshName: StringProperty(
        name='Mesh Name'
    )
    
    GWE_NewAnimationName: StringProperty(
        name=''
    )
    
    GWE_NumberOfAnimations: IntProperty(
        name=''
    )
    


    

    

# ------------------------------------------------------------------------
#    User Interface
# ------------------------------------------------------------------------
class AssetSettingsPanel(bpy.types.Panel):
    bl_idname = 'GWE_PT_EXPORTSETTINGSPANEL'
    bl_label = 'Export Settings'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GWE'

    def draw(self, context):
        layout = self.layout
        mytool = bpy.context.window_manager.GWE_tool
        
        exportNameRow = layout.row()
        exportNameRow.prop(mytool, 'GWE_ExportName')
        
        exportPathRow = layout.row()
        exportPathRow.prop(mytool, 'GWE_ExportPath')
        
        if (mytool.GWE_ExportTypeAnimationFake == '0'):
            exportTypeRow = layout.row()
            exportTypeRow.prop(mytool, 'GWE_ExportType')
        else:
            exportTypeRow = layout.row()
            exportTypeRow.prop(mytool, 'GWE_ExportTypeAnimationFake')
            exportTypeRow.enabled = False
        
        

class SkeletonToolsPanel(bpy.types.Panel):
    bl_idname = 'GWE_PT_SKELETONTOOLSPANEL'
    bl_label = 'Skeleton Tools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GWE'
    
    @classmethod
    def poll(cls, context):
        mytool = bpy.context.window_manager.GWE_tool
        if (mytool.GWE_ExportType == '2'):
            return True
        else:
            return False
        
    def draw(self, context):
        mytool = bpy.context.window_manager.GWE_tool
        layout = self.layout
        
        generateDeformationLabelRow = layout.row()
        generateDeformationLabelRow.label(text='Generate a Deformation Rig : ')
        
        
        controlRigPointerRow = layout.row()
        controlRigPointerRow.prop(mytool, 'GWE_ControlRigPointer')
        
        meshPointerRow = layout.row()
        meshPointerRow.prop(mytool, 'GWE_MeshPointer')
        
        deformationRigPointerRow = layout.row()
        deformationRigPointerRow.prop(mytool, 'GWE_DeformationRigPointer')
        
        op_generateDeformRigRow = layout.row()
        op_generateDeformRigRow.operator('object.skeleton_generate_deform_rig')
        
        generateAnimationLabelRow = layout.row()
        generateAnimationLabelRow.label(text='Generate a New Animation File : ')
        
        
        op_generateAnimationFileRow = layout.row()
        op_generateAnimationFileRow.operator('object.skeleton_generate_animation_file')
        
        
        layout.label(text='')
        layout.label(text='For debug purposes and not intended for regular use :')
        
        op_cleanCollectionsRow = layout.row()
        op_cleanCollectionsCol1 = op_cleanCollectionsRow.column()
        op_cleanCollectionsCol2 = op_cleanCollectionsRow.column()
        op_cleanCollectionsCol1.label(text='   {   DEBUG ONLY   }   ')
        op_cleanCollectionsCol2.operator('object.skeleton_clean_collection')

        op_disassembleRigRow = layout.row()
        op_disassembleRigCol1 = op_disassembleRigRow.column()
        op_disassembleRigCol2 = op_disassembleRigRow.column()
        op_disassembleRigCol1.label(text='   {   DEBUG ONLY   }   ')
        op_disassembleRigCol2.operator('object.skeleton_disassemble_rig')
        
        deformationRigPointerRow.enabled = False
        
        if (mytool.GWE_bRigGenerated):
            controlRigPointerRow.enabled = False
            meshPointerRow.enabled = False
            op_generateDeformRigRow.enabled = False
            generateDeformationLabelRow.enabled = False
        else:
            op_generateAnimationFileRow.enabled = False
            op_cleanCollectionsRow.enabled = False
            op_disassembleRigRow.enabled = False
            generateAnimationLabelRow.enabled = False
        

class SkeletonExportPanel(bpy.types.Panel):
    bl_idname = 'GWE_PT_SKELETONEXPORTPANEL'
    bl_label = 'Skeleton Export'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GWE'
    
    @classmethod
    def poll(cls, context):
        mytool = bpy.context.window_manager.GWE_tool
        if (mytool.GWE_ExportType == '2'):
            return True
        else:
            return False

    def draw(self, context):
        layout = self.layout
        layout.label(text="Exports Skeleton as Mesh and Armature")
        
        
class AnimationToolsPanel(bpy.types.Panel):
    bl_idname = 'GWE_PT_ANIMATIONTOOLSPANEL'
    bl_label = 'Animation Tools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GWE'
    
    @classmethod
    def poll(cls, context):
        mytool = bpy.context.window_manager.GWE_tool
        if (mytool.GWE_ExportTypeAnimationFake == '1'):
            return True
        else:
            return False
        
    def draw(self, context):
        mytool = bpy.context.window_manager.GWE_tool
        
        layout = self.layout
        
        setupAnimationFileLabelRow = layout.row()
        setupAnimationFileLabelRow.label(text='Setup Animation File :')
        
        linkedSkeletonFilePathRow = layout.row()
        linkedSkeletonFilePathRow.prop(mytool, 'GWE_AnimLinkedSkeletonFilePath')
        
        linkedSkeletonCollectionRow = layout.row()
        linkedSkeletonCollectionRow.prop(mytool, 'GWE_AnimLinkedSkeletonCollection')
        
        op_linkSkeletonRow = layout.row()
        op_linkSkeletonRow.operator('object.link_skeleton')
        
        linkedSkeletonFilePathRow.enabled = False
        linkedSkeletonCollectionRow.enabled = False
        
        if (mytool.GWE_bAnimLinked):
            op_linkSkeletonRow.enabled = False
            setupAnimationFileLabelRow.enabled = False
        
            
class AnimationLibraryPanel(bpy.types.Panel):
    bl_idname = 'GWE_PT_ANIMATIONLIBRARYPANEL'
    bl_label = 'Animation Library'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GWE'
    
    @classmethod
    def poll(cls, context):
        mytool = bpy.context.window_manager.GWE_tool
        if (mytool.GWE_ExportTypeAnimationFake == '2'):
            return True
        else:
            return False
    
    def draw(self, context):
        mytool = bpy.context.window_manager.GWE_tool
        
        layout = self.layout
        
        
        
        layout.template_list('GWE_UL_AnimationSceneList', '', bpy.data, "scenes", bpy.context.window_manager, 'GWE_AnimationListIndex', type='DEFAULT')        
        
        animationSceneToolsRow = layout.row()
        
        animationSceneToolsRow.operator('object.move_animation_scene_up')
        animationSceneToolsRow.operator('object.move_animation_scene_down')
        animationSceneToolsRow.operator('object.rename_animation_scene')
        animationSceneToolsRow.operator('object.delete_animation_scene')
        
        
        layout.label(text='')
        addAnimationRow = layout.row()
        addAnimationCol1 = addAnimationRow.column()
        addAnimationCol2 = addAnimationRow.column()
        addAnimationCol1.prop(mytool, 'GWE_NewAnimationName')
        addAnimationCol2.operator('object.add_animation_scene')             
        
        
        

# ------------------------------------------------------------------------
#    Lists
# ------------------------------------------------------------------------
class GWE_UL_AnimationSceneList(bpy.types.UIList):
        
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
            
        row = layout.row(align=True)
        
        name = item.name
        row.prop(item, "GWE_AnimationName", text='', emboss=False)
        
        
        
    
    


# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------
class GWE_OT_SkeletonGenerateDeformRigBtn(bpy.types.Operator):
    bl_label = 'Generate Deform Rig'
    bl_idname = 'object.skeleton_generate_deform_rig'
    
    
    
    def execute(self, context):        
        mytool = bpy.context.window_manager.GWE_tool
        
        if (mytool.GWE_ControlRigPointer.type != "ARMATURE"):
            raise Exception("Control Rig is not set to an armature...")
        
        if (mytool.GWE_MeshPointer.type != 'MESH'):
            raise Exception("Mesh is not set to a mesh...")
            
        #need to have something selected or I can't go into object mode apparantly.  
        bpy.context.view_layer.objects.active = mytool.GWE_MeshPointer
        
        bpy.ops.object.mode_set(mode='OBJECT')
        
        ctrl_rig = mytool.GWE_ControlRigPointer
        
        bpy.ops.object.select_all(action='DESELECT')
        ctrl_rig.select_set(True)
        bpy.context.view_layer.objects.active = ctrl_rig
                
        bpy.ops.object.duplicate()
        
        def_rig = bpy.context.object
        
        bpy.ops.object.mode_set(mode='EDIT')
        
        #iterate through all the bones of our newly duplicated mesh and remove non-deforming bones
        for bone in bpy.context.object.data.edit_bones[:]:
            if not bone.name.lower().startswith('def-'):
                bpy.context.object.data.edit_bones.remove(bone)
                
        #remove all constraints on pose bones and add new copy transform constraints to the control rig
        for bone in bpy.context.object.pose.bones[:]:
            for c in bone.constraints:
                bone.constraints.remove(c)
            cpytf = bone.constraints.new('COPY_TRANSFORMS')
            cpytf.target = ctrl_rig
            cpytf.subtarget = bone.name
            
        #go back to object mode, change layer so we can see def rig bones, change names of ctrl rig an def rig
        
        bpy.ops.object.mode_set(mode='OBJECT')
        
        ctrl_rig.name = 'ctrl-rig'
        ctrl_rig.data.name = 'ctrl-rig'
        
        def_rig.name = 'def-rig'
        def_rig.data.name = 'def-rig'
        
        def_rig.data.layers[29] = True
        for i in range(0, 31):
            if i != 29:
                def_rig.data.layers[i] = False
                
        mesh = mytool.GWE_MeshPointer
        
        bpy.ops.object.select_all(action='DESELECT')
        mesh.select_set(True)
        def_rig.select_set(True)
        bpy.context.view_layer.objects.active = def_rig
        
        bpy.ops.object.parent_set(type='ARMATURE_AUTO')
        
        #move all three objects to a new collection...delete any collections that these objects belonged to and unlink them from the scene (as they will be linked to a collection)
        for c in ctrl_rig.users_collection:
            if c == bpy.context.scene.collection:
                c.objects.unlink(ctrl_rig)
            else:
                bpy.data.collections.remove(c)
            
        for c in def_rig.users_collection:
            if c == bpy.context.scene.collection:
                c.objects.unlink(def_rig)
            else:
                bpy.data.collections.remove(c)
            
        for c in mesh.users_collection:
            if c == bpy.context.scene.collection:
                c.objects.unlink(mesh)
            else:
                bpy.data.collections.remove(c)
            
            
        newCollection = bpy.data.collections.new(name='Blender Skeleton')
        bpy.context.scene.collection.children.link(newCollection)
        
        newCollection.objects.link(ctrl_rig)
        newCollection.objects.link(def_rig)
        newCollection.objects.link(mesh)
        
        mytool.GWE_DeformationRigPointer = def_rig
        mytool.GWE_bRigGenerated = True
        
        
       
        return {'FINISHED'}

class GWE_OT_SkeletonGenerateAnimationFile(bpy.types.Operator):
    bl_label = 'Generate Animation File'
    bl_idname = 'object.skeleton_generate_animation_file'
    
    def execute(self, context):
        mytool = bpy.context.window_manager.GWE_tool
        
    
        if bpy.data.is_dirty:
            raise Exception('Please save this skeleton file before trying to generate an animation as this file will close')
            
        #check to make sure we have a collection consisting of and only of the control rig, deformation rig, and mesh...
        if len(mytool.GWE_MeshPointer.users_collection) != 1 or len(mytool.GWE_DeformationRigPointer.users_collection) != 1 or len(mytool.GWE_ControlRigPointer.users_collection) != 1:
            raise Exception('One of your rigs belongs to more than one collection...')
        
        #get the collection mesh pointer is and verify that collection only consists of the deformation and control rig...
        collectionTest = mytool.GWE_MeshPointer.users_collection[0]
        
        for obj in collectionTest.all_objects:
            if (obj != mytool.GWE_DeformationRigPointer) and (obj != mytool.GWE_ControlRigPointer) and (obj != mytool.GWE_MeshPointer):
                print(obj.name)
                raise Exception('You have another object in the rig collection that should not be there...')
            
            

        
        #We're going to create a new file...start by pulling any data we will need for the new file... 
        skFilePath = bpy.data.filepath
        skCollection = collectionTest.name
        
        skControlRigName = mytool.GWE_ControlRigPointer.name
        skDeformationRigName = mytool.GWE_DeformationRigPointer.name
        skMeshName = mytool.GWE_MeshPointer.name
        
        bpy.ops.wm.read_homefile()
        
        mytool = bpy.context.window_manager.GWE_tool
                
        mytool.GWE_AnimLinkedSkeletonFilePath = skFilePath
        mytool.GWE_AnimLinkedSkeletonCollection = skCollection
        mytool.GWE_ExportTypeAnimationFake = '1'
        
        mytool.GWE_ControlRigName = skControlRigName
        mytool.GWE_DeformationRigName = skDeformationRigName
        mytool.GWE_MeshName = skMeshName
        
        return {'FINISHED'}
    
        
    
class GWE_OT_SkeletonDisassembleRig(bpy.types.Operator):
    bl_label = '{ Disassemble Rig }'
    bl_idname = 'object.skeleton_disassemble_rig'
    
    def execute(self, context):
        mytool = bpy.context.window_manager.GWE_tool
        
        bpy.ops.object.mode_set(mode='OBJECT')
        
        #select and unparent the base mesh rig
        bpy.ops.object.select_all(action='DESELECT')
        mytool.GWE_MeshPointer.select_set(True)
        bpy.context.view_layer.objects.active = mytool.GWE_MeshPointer
        
        bpy.ops.object.parent_clear(type='CLEAR')
        
        #select and delete the deformation rig and set the pointer to None
        bpy.ops.object.select_all(action='DESELECT')
        mytool.GWE_DeformationRigPointer.select_set(True)
        bpy.context.view_layer.objects.active = mytool.GWE_DeformationRigPointer
        
        bpy.data.objects.remove(mytool.GWE_DeformationRigPointer)
        
        #perhaps unnecessary
        mytool.GWE_DeformationRigPointer = None
        
        mytool.GWE_bRigGenerated = False
        
        return {'FINISHED'}
    
class GWE_OT_SkeletonCleanCollection(bpy.types.Operator):
    bl_label = '{ Clean Collections }'
    bl_idname = 'object.skeleton_clean_collection'
    
    def execute(self, context):
        mytool = bpy.context.window_manager.GWE_tool
        
        ctrl_rig = mytool.GWE_ControlRigPointer
        def_rig = mytool.GWE_DeformationRigPointer
        mesh = mytool.GWE_MeshPointer
        
        for c in ctrl_rig.users_collection:
            if c == bpy.context.scene.collection:
                c.objects.unlink(ctrl_rig)
            else:
                bpy.data.collections.remove(c)
            
        for c in def_rig.users_collection:
            if c == bpy.context.scene.collection:
                c.objects.unlink(def_rig)
            else:
                bpy.data.collections.remove(c)
            
        for c in mesh.users_collection:
            if c == bpy.context.scene.collection:
                c.objects.unlink(mesh)
            else:
                bpy.data.collections.remove(c)
            
            
        newCollection = bpy.data.collections.new(name='Blender Skeleton')
        bpy.context.scene.collection.children.link(newCollection)
        
        newCollection.objects.link(ctrl_rig)
        newCollection.objects.link(def_rig)
        newCollection.objects.link(mesh)
        
        
        return {'FINISHED'}
    
    
class GWE_OT_AnimationLinkSkeleton(bpy.types.Operator):
    bl_label = 'Link Skeleton'
    bl_idname = 'object.link_skeleton'
    
    
    def execute(self, context):
        mytool = bpy.context.window_manager.GWE_tool
        
        #Link All Objects we need
        #This must be done with a button because it glitches out if we try to do it directly after the plugin creates a new file...
        bpy.ops.wm.link(directory=mytool.GWE_AnimLinkedSkeletonFilePath + '\\Collection\\', filename=mytool.GWE_AnimLinkedSkeletonCollection)
        
        linkedObject = bpy.data.objects.get(mytool.GWE_AnimLinkedSkeletonCollection)

        bpy.ops.object.select_all(action='DESELECT')
        linkedObject.select_set(True)
        bpy.context.view_layer.objects.active = linkedObject
        
        bpy.ops.object.make_override_library()
        
        #assign this file's pointers to the skeleton components as they could not be perserved from the skeleton file...
        mytool.GWE_ControlRigPointer = bpy.data.objects.get(mytool.GWE_ControlRigName)
        mytool.GWE_DeformationRigPointer = bpy.data.objects.get(mytool.GWE_DeformationRigName)
        mytool.GWE_MeshPointer = bpy.data.objects.get(mytool.GWE_MeshName)
        
        mytool.GWE_bAnimLinked=True


        print("HELLLOOOOOO")
        #after we have linked our skeleton file, set up an initial animation scene, assign fake users and remove the scene...
        bpy.ops.object.add_initial_animation_scene()
        
        mytool.GWE_ExportTypeAnimationFake = '2'
        
                
        return {'FINISHED'}
    
#very redundant...most of this and add_animation_scene can be combined into one operator
#but it works and I'm lazy
class GWE_OT_AddInitialAnimationScene(bpy.types.Operator):
    bl_label = 'Add Initial Animation'
    bl_idname = 'object.add_initial_animation_scene'
    
    def execute(self, context):
        mytool = bpy.context.window_manager.GWE_tool

        #animation counter starts at zero because that's the default for an int.  We actually want it to start at 1 for clarity
        mytool.GWE_NumberOfAnimations += 1
        
        
        digitsAnimCount = len(str(mytool.GWE_NumberOfAnimations))
        animCountText = mytool.GWE_NumberOfAnimations            
        
        anim = 'idle'
        animSceneName = '.' + '00' + str(mytool.GWE_NumberOfAnimations) + '-' + anim
        
        #we need to enforce that the animation does not already exist, or I can't 'get' a pointer to the new scene
        if (bpy.data.scenes.get(animSceneName)):
            raise Exception('Animation of this name already exists')
            
            
        #create a new scene, duplicate the deformation rig, rename to match animation, move to new scene, append to list of animations...
        bpy.data.scenes.new(animSceneName)
        
        animScene = bpy.data.scenes.get(animSceneName)
        
        ctrl_rig = mytool.GWE_ControlRigPointer
        def_rig = mytool.GWE_DeformationRigPointer
        mesh = mytool.GWE_MeshPointer
    
        bpy.ops.object.select_all(action='DESELECT')
        def_rig.select_set(True)
        mesh.select_set(True)
        bpy.context.view_layer.objects.active = def_rig
        
        bpy.ops.object.duplicate()
        
        animRig = bpy.context.selected_objects[0]
        animMesh = bpy.context.selected_objects[1]
        
        animRig.name = 'anim-' + anim
        animRig.data.name = 'anim-' + anim
        
        #I don't know why...but for the animRig data we can rename it but with the mesh data
        #if we do that the linked library gets confused...
        animMesh.name = 'mesh-' + anim
        #animMesh.data.name = 'mesh-' + anim
        
        animRig.users_scene[0].collection.objects.unlink(animRig)
        animMesh.users_scene[0].collection.objects.unlink(animMesh)
        
        animScene.collection.objects.link(animRig)
        animScene.collection.objects.link(animMesh)
        
        #for our first scene...delete the initial scene and assign fake users to def-rig and mesh so they don't get deleted
        def_rig.use_fake_user = True
        mesh.use_fake_user = True
        
        #bring control rig with us.  Remove from any collection it is in and move to our scene
        for c in ctrl_rig.users_collection:
            c.objects.unlink(ctrl_rig)
        animScene.collection.objects.link(ctrl_rig)
        
        #travel to new scene, delete old scene
        initialScene = bpy.context.window.scene        
        bpy.context.window.scene = animScene
        
        bpy.data.scenes.remove(initialScene)
        
        
        #select control rig, assign a new action to ctrl rig, go into pose mode...
        bpy.ops.object.select_all(action='DESELECT')
        ctrl_rig.select_set(True)
        bpy.context.view_layer.objects.active = ctrl_rig
        
        newAction = bpy.data.actions.new('ctrl-' + anim)
        ctrl_rig.animation_data.action = newAction
        
        bpy.ops.object.mode_set(mode='POSE')
        
        #assign animation name so we can show it in a list without '.'
        animScene.GWE_AnimationName = anim
        
        #increment scene counter for naming convention
        mytool.GWE_NumberOfAnimations += 1
        
        
        return {'FINISHED'}
    
class GWE_OT_AddAnimationScene(bpy.types.Operator):
    bl_label = 'Add Animation'
    bl_idname = 'object.add_animation_scene'
    
    def execute(self, context):
        mytool = bpy.context.window_manager.GWE_tool
        
        #ensure that actually remembered to put a name in...
        if (len(mytool.GWE_NewAnimationName) == 0):
            raise Exception('Please specify a name for the new animation')
        
        #we need to enforce that the animation does not already exist, or I can't 'get' a pointer to the new scene
        if (bpy.data.scenes.get('.'+mytool.GWE_NewAnimationName)):
            raise Exception('Animation of this name already exists')
            
            
        animSceneName = '.' + str(mytool.GWE_NumberOfAnimations) + '-' + mytool.GWE_NewAnimationName  
        
        digitsAnimCount = len(str(mytool.GWE_NumberOfAnimations))
        
        #preload 0's for sorting purposes
        for i in range(0, 3-digitsAnimCount):
            animSceneName = animSceneName[0] + '0' + animSceneName[1:]
        
        #create a new scene, duplicate the deformation rig, rename to match animation, move to new scene, append to list of animations...
        bpy.data.scenes.new(animSceneName)
        
        animScene = bpy.data.scenes.get(animSceneName)
        
        #create a temporary scene to bring our old def-rig and mesh to duplicate...
        bpy.data.scenes.new(name='.GWE_VOID')
        voidScene = bpy.data.scenes.get('.GWE_VOID')
        
        ctrl_rig = mytool.GWE_ControlRigPointer
        def_rig = mytool.GWE_DeformationRigPointer
        mesh = mytool.GWE_MeshPointer
        
        #bring us and our def_rig and mesh into the void
        bpy.context.window.scene = voidScene
        voidScene.collection.objects.link(def_rig)
        voidScene.collection.objects.link(mesh)
        
        #duplicate def_rig and mesh
        bpy.ops.object.select_all(action='DESELECT')
        def_rig.select_set(True)
        mesh.select_set(True)
        bpy.context.view_layer.objects.active = def_rig
        
        bpy.ops.object.duplicate()
        
        #Renaming...
        animRig = bpy.context.selected_objects[0]
        animMesh = bpy.context.selected_objects[1]
        
        animRig.name = 'anim-' + mytool.GWE_NewAnimationName
        animRig.data.name = 'anim-' + mytool.GWE_NewAnimationName
        
        #I don't know why...but for the animRig data we can rename it but with the mesh data
        #if we do that the linked library gets confused...
        animMesh.name = 'mesh-' + mytool.GWE_NewAnimationName
        #animMesh.data.name = 'mesh-' + mytool.GWE_NewAnimationName
        
        
        #push our duplicated objects into a new scene
        animRig.users_scene[0].collection.objects.unlink(animRig)
        animMesh.users_scene[0].collection.objects.unlink(animMesh)
        
        animScene.collection.objects.link(animRig)
        animScene.collection.objects.link(animMesh)
        
        #bring control rig with us.  Remove from any collection it is in and move to our scene
        for c in ctrl_rig.users_collection:
            c.objects.unlink(ctrl_rig)
        animScene.collection.objects.link(ctrl_rig)
        
        #travel to new scene, delete old scene
        initialScene = bpy.context.window.scene        
        bpy.context.window.scene = animScene
        
        bpy.data.scenes.remove(initialScene)
        
        
        #select control rig, assign a new action to ctrl rig, go into pose mode...
        bpy.ops.object.select_all(action='DESELECT')
        ctrl_rig.select_set(True)
        bpy.context.view_layer.objects.active = ctrl_rig
        
        newAction = bpy.data.actions.new('ctrl-' + mytool.GWE_NewAnimationName)
        ctrl_rig.animation_data.action = newAction
        
        bpy.ops.object.mode_set(mode='POSE')
        
        #assign animation name so we can show it in a list without '.'
        animScene.GWE_AnimationName = mytool.GWE_NewAnimationName
        
        #set new animation name property to nothing for visual purposes
        mytool.GWE_NewAnimationName = ''
        
        #increment scene counter for naming convention
        mytool.GWE_NumberOfAnimations += 1
        
        print(mytool.GWE_NumberOfAnimations)
        #change to our newly created scene for convenience
        bpy.context.window_manager.GWE_AnimationListIndex = mytool.GWE_NumberOfAnimations - 2
        
        return {'FINISHED'}
    
def gwe_SwapAnimationScenes(xIndex, yIndex):
        xScene = bpy.data.scenes[xIndex]
        yScene = bpy.data.scenes[yIndex]
        
        #find number of digits our scenes are
        xDigits = len(str(xIndex+1))
        yDigits = len(str(yIndex+1))
        
        xSceneName = '.' + str(yIndex+1) + '-' + xScene.GWE_AnimationName
        ySceneName = '.' + str(xIndex+1) + '-' + yScene.GWE_AnimationName
        
        #preload 0's for sorting purposes
        for i in range(0, 3-yDigits):
            xSceneName = xSceneName[0] + '0' + xSceneName[1:]
            
        #preload 0's for sorting purposes
        for i in range(0, 3-xDigits):
            ySceneName = ySceneName[0] + '0' + ySceneName[1:]
        
        xScene.name = '.GWE_temp'
        yScene.name = '.GWE_tempBack'
        
        xScene.name = xSceneName
        yScene.name = ySceneName
    
class GWE_OT_MoveAnimationSceneUp(bpy.types.Operator):
    bl_label = '↑'
    bl_idname = 'object.move_animation_scene_up'
    
    sceneName : StringProperty(default='')
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        index = bpy.context.window_manager.GWE_AnimationListIndex
        
        #if we are already at the top of the stack, button does nothing...
        if (index == 0):
            print('Cannot move scene up.  Scene is already at the top of the stack')
            return {'FINISHED'}
        
        gwe_SwapAnimationScenes(index, index-1)
        
        bpy.context.window_manager.GWE_AnimationListIndex -= 1
    
        return {'FINISHED'}
    
class GWE_OT_MoveAnimationSceneDown(bpy.types.Operator):
    bl_label = '↓'
    bl_idname = 'object.move_animation_scene_down'
    
    sceneName : StringProperty(default='')
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):        
        index = bpy.context.window_manager.GWE_AnimationListIndex
        
        #if we are already at the top of the stack, button does nothing...
        if (index + 1 == len(bpy.data.scenes)):
            print('Cannot move scene down.  Scene is already at the bottom of the stack')
            return {'FINISHED'}
        
        gwe_SwapAnimationScenes(index, index+1)
        
        bpy.context.window_manager.GWE_AnimationListIndex += 1
            
        return {'FINISHED'}

    
class GWE_OT_RenameAnimationScene(bpy.types.Operator):
    bl_label = 'R'
    bl_idname = 'object.rename_animation_scene'
    
    sceneName : StringProperty(default='')
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        mytool = bpy.context.window_manager.GWE_tool
        
        print(self.sceneName)
        
        return {'FINISHED'}
    
class GWE_OT_DeleteAnimationScene(bpy.types.Operator):
    bl_label = 'X'
    bl_idname = 'object.delete_animation_scene'
    
    sceneName : StringProperty(default='')
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        mytool = bpy.context.window_manager.GWE_tool
        
        print(self.sceneName)
        
        return {'FINISHED'}
    
# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------
classes = (
    GWE_Properties,
    AssetSettingsPanel,
    SkeletonToolsPanel,
    SkeletonExportPanel,
    AnimationToolsPanel,
    AnimationLibraryPanel,
    
    GWE_OT_SkeletonGenerateDeformRigBtn,
    GWE_OT_SkeletonGenerateAnimationFile,
    GWE_OT_SkeletonCleanCollection,
    GWE_OT_SkeletonDisassembleRig,
    GWE_OT_AnimationLinkSkeleton,
    GWE_OT_AddInitialAnimationScene,
    GWE_OT_AddAnimationScene,
    GWE_OT_MoveAnimationSceneUp,
    GWE_OT_MoveAnimationSceneDown,
    GWE_OT_RenameAnimationScene,
    GWE_OT_DeleteAnimationScene,    
    
    GWE_UL_AnimationSceneList
    )

def gwe_SwitchAnimationScene(self, context):
    
    index = bpy.context.window_manager.GWE_AnimationListIndex
    
    mytool = bpy.context.window_manager.GWE_tool
    
    scene = bpy.data.scenes[index]
        
    ctrl_rig = mytool.GWE_ControlRigPointer
        
    #travel to new scene, bringing control rig with you
    for c in ctrl_rig.users_collection:
        c.objects.unlink(ctrl_rig)
    scene.collection.objects.link(ctrl_rig)
    
    bpy.context.window.scene = scene
        
    bpy.ops.object.select_all(action='DESELECT')
    ctrl_rig.select_set(True)
    bpy.context.view_layer.objects.active = ctrl_rig
    
    #set our ctrl_rig to use the proper action...
    
    ctrl_rig.animation_data.action = bpy.data.actions.get('ctrl-' + scene.GWE_AnimationName)
    
    #go to pose mode
    bpy.ops.object.mode_set(mode='POSE')
    
    return


def menu_func(self, context):
    self.layout.operator(ExportPanel.bl_idname)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.WindowManager.GWE_tool = PointerProperty(type=GWE_Properties)
    bpy.types.Object.GWE_serializer = PointerProperty(type=GWE_Properties)
    
    bpy.types.WindowManager.GWE_AnimationListIndex = IntProperty(update=gwe_SwitchAnimationScene)
    bpy.types.Scene.GWE_AnimationName = StringProperty(default='')

    bpy.app.handlers.save_pre.append(GWE_SaveHandler)
    bpy.app.handlers.load_post.append(GWE_LoadHandler)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.WindowManager.GWE_tool
    #kinda want to keep this in case plugin gets removed so the file doesn't lose all its data...
    #del bpy.types.Object.GWE_serializer
    
    del bpy.types.WindowManager.GWE_AnimationListIndex
    del bpy.types.Scene.GWE_AnimationName

    bpy.app.handlers.save_pre.remove(GWE_SaveHandler)
    bpy.app.handlers.load_post.remove(GWE_LoadHandler)

if __name__ == "__main__":
    register();

