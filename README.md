# perspective-scene-blender-addon
Blender python script to create a 3D scene with customizable subject, camera, environment options.

## How to use
The add-on will be available to use from the sidebar panel (of the 3D viewport) as a tab named 'Perspective Scene' 
[place cursor in 3D viewport, press 'N' top open sidebar panel]

### Specific Instructions
1. Download the zip file, extract files.
3. Install the addon in Blender under Edit > Preferences > Install (choose the **perspective_scene_generation_addon_v1.py** file)
4. Check (select) the Perspective Scene Generation addon (found as 'Add Mesh: Perspective Scene addon')
5. Hover mouse in 3D Viewport, press 'N' to open the sidebar
6. Perspective Scene addon is visible on the sidebar and ready for use

## Add-on Motivation
There has been an increasing interest in prompt engineering to create AI-generated images. While trying out such language-to-image models (which produces synthetic images via text and optional image prompting), it was observed that although the subject of the prompt was mostly accurately identified, the model had little sensitivity to distance specifications with respect to the subject. All images generated from the model put the subject as the main focus of the generated image, regardless of distance specifications.

While this add-on does not incorporate AI methods, it aims to provide a means for generating images which takes into account the distance and angle between the camera and the subject specified (among other customizable features described below).

## Add-on Description
The parameters of the add-on can be best understood through this text prompt template which references the following image:

<img width="283" alt="botmid_3sub_far" src= "https://user-images.githubusercontent.com/65459827/204546533-54fc1146-8d02-4be1-9a70-a8ddd8c52111.png">    
    
    "[2 (subject quantity)] [house (subject)]s in the [middle_right (quadrant)] section of the scene's plane, 
    where the camera is [Near (distance from camera)] the subject and the scene is 
    populated with particles of other objects in the [env1 choices] collections. 
    
    [particle_count] is the number of these objects that belong to the 
    specified environment collection which are generated on the portion of the plane 
    (which is fully visible to the camera) according to the [particle_scale].
    
    Where an environment collection is not available in the scene, it is recommended to have the selection boxes for 
    [Generate example collection] and [Use example collection] checked.
    
    The desired [camera x rotation] (tilting to face the plane) can be customizable from a range of 30-60 degrees.
    
    The [render image] checkbox is available to opt for rendering an image of the camera view of the generated scene.
    
    2 options [colour_1] and [colour_2] for base colours are provided to be mixed 
    for a random base plane material shader with a mixture of the 2 colours specified."
    
## Important Notes: 
The current tool's logic prioritises [Generate sample collection] over the environment collection selection. 
(i.e. if you do not have an existing collection of objects (to be used as environment collection) in Blender and want to see how the code works, do:
**Check BOTH the [Generate example collection] and [Use example collection] boxes.**
Note: by default, the Generate example collection and Use example collection boxes are **UNCHECKED**.

<img width="155" alt="image" src="https://user-images.githubusercontent.com/65459827/204555406-5a98f05c-e41b-491e-b344-9866f501ed69.png">

Safer to click 'Scene collection' in the outliner right before generating the scene so that no other object is selected when the script runs. (might lead to unexpected errors)

<img width="159" alt="image" src="https://user-images.githubusercontent.com/65459827/204555097-797d9f7d-4420-403c-a8b7-f9d61b642b14.png">

### The valid arguments for the customizable parameters are listed as follows: 
theChosenObject (the Subject of the scene): 
    
    any object in the scene

Quadrant (the portion of the plane that fits within the camera view sectioned as a 3 x 3 grid; subject mesh(es) will be instantiated at the specified quadrant): 

    top left, top middle, top right, middle left, middle middle, middle right, bottom left, bottom middle, bottom right
    
Subject quantity valid range (number of subject meshes that can be instantiated in the specified quadrant): 

    1-3

Distance categories available (distance of camera to the subject mesh): 

    Near, Moderate, Far

camera x rotation angle valid range (the tilt of the camera when facing the plane/scene to be rendered): 

    30-60 degrees (about the X-axis)

base colour vectors: 
    
    (0.0, 0.0, 0.0) to (1.0, 1.0, 1.0) colour vector coordinates
    
#### Quadrant Description and Illustration 
Subject mesh(es) will be instantiated at the specified quadrant.
In the context of the quadrant parameter, the 3 x 3 grid is as illustrated below:

<img width="283" alt="botmid_3sub_far_grid" src= "https://user-images.githubusercontent.com/65459827/204558210-17f46320-b280-4f5f-8b43-c1002f7623d3.jpg">

## Sample images that can be generated
Note: 
Sample Image uses an env1_choices collection which contains 2 types of tree meshes and a house mesh object selected as the subject (theChosenObject)

<img width="283" alt="botmid_3sub_far" src="https://user-images.githubusercontent.com/65459827/204551511-a39603ee-b6ee-48e5-8d25-e2ad1a83c911.png"> <img width="663" alt="botmid_3sub_far" src="https://user-images.githubusercontent.com/65459827/204551675-a9d579ee-8687-42f3-b6b1-ac2b7f03b024.jpg">

### Rendered images filepath
Rendered images are labelled by the timestamp in the render filepath folder location specified in the render settings.

### Render engine
Default render engine is Cycles with GPU compute if GPU is available on the local machine. 
Otherwise, Eevee render engine is used to render images (may result in images with strobing effect of the background plane)

### Potential misalignment of environment objects particle system on plane surface:
To fix the misalignment of the environment collection's particle system:

select the relevant object in the environment collection > tab into edit mode > press G key > press X key then move mouse to adjust the particle system to be at the desired Z location > click to finalise particle system Z location. 

### Additional notes:
This add-on was created with the image of natural scenes in mind. Hence, [colour_1] and [colour_2] are pre-set to green and brown respectively. 
A limitation of this add-on is that colours have to be specified by colour vector coordinates (0.0-1.0).
   
This add-on was created using Blender version 3.1.2 

## Future Refinements/Additional Features/Bug Fixes
Subject meshes instantiated (if >1) might experience collisions. (not sure)

