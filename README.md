# perspective-scene-blender-addon
Blender python script to create a 3D scene with customizable subject, camera, environment options.

## Add-on Motivation
There has been an increasing interest in prompt engineering to create AI-generated images. While trying out DiscoDiffusion model, a model which produces synthetic images via text (and optional image) prompting, it was observed that although the subject of the prompt was mostly accurately identified, the model had little sensitivity to distance specifications with respect to the subject. All images generated from the model put the subject as the main focus of the generated image, regardless of distance specifications.

While this add-on does not incorporate AI methods, it aims to provide a means for generating images which take into account the distance and angle between the camera and the subject specified (among other customizable features described below).

## Add-on Description
The parameters of the add-on can be best understood through this text prompt template which references the following image:

    "[2] [house]s in the [middle_right] section of the scene's plane, where the camera is [Neat] the subject and the scene is populated with particles of other objects in the [env1 choices] collections. 
    
    [particle_count] is the number of these objects that belong to the specified environment collection which are generated on the portion of the plane (which is fully visible to the camera) according to the [particle_scale].
    
    Where an environment collection is not available in the scene, it is recommended to have the selection boxes for [generate example collection] and [use example collection] checked.
    
    The desired [camera x rotation] (tilting to face the plane) can be customizable from a range of 30-60 degrees.
    
    The [render image] checkbox is available to opt for rendering an image of the camera view of the generated scene.
    
    2 options [colour_1] and [colour_2] for base colours are provided to be mixed for a random base plane material shader with a mixture of the 2 colours specified."
    
### Additional notes:
    This add-on was created with the image of natural scenes in mind. Hence, [colour_1] and [colour_2] are pre-set to green and brown respectively. 
    A limitation of this add-on is that colours have to be specified by colour vector coordinates (0.0-1.0).
    

### The valid arguments for the customizable parameters are listed as follows: 

Subject quantity valid range: 1-3
Distance categories available: NEAR, MODERATE, FAR
Angle valid range: 30-60 degrees (about the X-axis)

## How to use
1. download the perspective_scene.py file, 
2. open it in blender, scripting tab
3. run the script
the add-on will be available to use from the sidebar panel (of the 3D viewport) as a tab named 'Perspective Scene' 
[place cursor in 3D viewport, press 'N' top open sidebar panel]

(Current script is unable to be imported as an add-on because Blender restricts access to bpy.context and bpy.data. 
--> need code refactoring to update the addon to access the context during execution rather then on registration.)

## Future Refinements/Additional Features/Bug Fixes

