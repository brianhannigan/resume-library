# 3D Visualization and Control Demo

A lightweight visualization tool demonstrating how to load 3D geometry, render it interactively, and provide user control over rotation, zoom, and view toggles.

## Overview
This project shows real-time 3D rendering and interaction logic using C# and Unity, similar to components developed in secure simulation systems.

## Key Features
- Load and display 3D geometry from STL or mesh data
- Modular C# scripts for rendering and control
- Camera orbit, zoom, and rotation interaction
- Real-time performance monitoring and feedback
- Extensible architecture for future geometry and control logic

## Folder Structure
```
/3DVisualizationDemo
 ├─ Assets/
 │   ├─ Scripts/
 │   │   ├─ STLImporter.cs
 │   │   ├─ CameraController.cs
 │   │   ├─ ObjectManager.cs
 │   ├─ Models/
 │   │   └─ sample.stl
 │   ├─ Scenes/
 │       └─ Main.unity
 ├─ README.md
 └─ LICENSE
```

## Sample Code Snippets

**STLImporter.cs**
```csharp
public Mesh ImportSTL(string filePath)
{
    var mesh = new Mesh();
    using (var reader = new BinaryReader(File.Open(filePath, FileMode.Open)))
    {
        reader.ReadBytes(80);
        uint triangles = reader.ReadUInt32();
        Vector3[] verts = new Vector3[triangles * 3];
        int[] indices = new int[triangles * 3];

        for (int i = 0; i < triangles; i++)
        {
            reader.ReadBytes(12);
            for (int v = 0; v < 3; v++)
            {
                float x = reader.ReadSingle();
                float y = reader.ReadSingle();
                float z = reader.ReadSingle();
                verts[i * 3 + v] = new Vector3(x, y, z);
                indices[i * 3 + v] = i * 3 + v;
            }
            reader.ReadUInt16();
        }

        mesh.vertices = verts;
        mesh.triangles = indices;
        mesh.RecalculateNormals();
    }
    return mesh;
}
```

**CameraController.cs**
```csharp
void Update()
{
    if (Input.GetMouseButton(0))
    {
        float rotX = Input.GetAxis("Mouse X") * 100f * Time.deltaTime;
        float rotY = Input.GetAxis("Mouse Y") * 100f * Time.deltaTime;
        transform.RotateAround(Vector3.zero, Vector3.up, rotX);
        transform.RotateAround(Vector3.zero, Vector3.right, rotY);
    }
    float scroll = Input.GetAxis("Mouse ScrollWheel");
    transform.Translate(0, 0, scroll * 2f, Space.Self);
}
```

## Usage
Run the Unity scene, load a sample STL, and explore the interactive 3D model with mouse rotation and zoom.

## License
MIT License
