import streamlit as st
from math import gcd
import sympy as sp
def simp_frac(nums, D):
    ret = []
    for coordinate in nums:
        if coordinate%D != 0:
            gcf = gcd(coordinate, D)
            n=round(coordinate/gcf)
            d=round(D/gcf)
            if d < 0 and n < 0:
                n = abs(n)
                d = abs(d)
            ret.append(str(f"{n}/{d}"))
        else:
            ret.append(round(coordinate/D))
    return ret

st.title("Matrix Solver (Cramer's Method)")
type = st.selectbox("Matrix Size", ["2x2", "3x3"])
if type == "2x2":
    container=st.container(border=True)
    col1, col2, col3 = container.columns(3)
    e = {}
    for gg in range(1,3):
        x1 = col1.number_input("X coefficient", value=0, key=f"x1{gg}")
        y1 = col2.number_input("Y coefficient", value=0, key=f"y1{gg}")
        sol1 = col3.number_input("Solution", value=0, key=f"sol{gg}")
        e[f"a{gg}1"] = x1
        e[f"a{gg}2"] = y1
        e[f"s{gg}"] = sol1
    if st.button("Calculate"):
        D = (e["a11"] * e["a22"])-(e["a21"] * e["a12"])
        Dx = (e["s1"] * e["a22"])-(e["s2"] * e["a12"])
        Dy = (e["a11"] * e["s2"])-(e["a21"] * e["s1"])
            
        if D == 0:
            if Dx == 0 and Dy == 0:
                st.info("This Matrix has infinite solutions!")
                st.success("(IR, IR)")
            else:
                st.error("No Solution")
        else:
            Dx, Dy = simp_frac([Dx, Dy], D)
            st.success(f"({Dx}, {Dy})")
    
elif type == "3x3":
    container=st.container(border=True)
    col1, i1, col2, i2, col3, i3, col4 = container.columns(7)
    e = {}
    for gg in range(1,4):
        col1, i1, col2, i2, col3, i3, col4 = container.columns(7)
        x1 = col1.number_input("", value=0, key=f"x1{gg}")
        i1.markdown("")
        i1.subheader("  X + ")
        y1 = col2.number_input("", value=0, key=f"y1{gg}")
        i2.markdown("")
        i2.subheader("  Y + ")
        z1 = col3.number_input("", value=0, key=f"z1{gg}")
        i3.markdown("")
        i3.subheader("  Z = ")
        sol1 = col4.number_input("", value=0, key=f"sol{gg}")
        e[f"a{gg}1"] = x1
        e[f"a{gg}2"] = y1
        e[f"a{gg}3"] = z1
        e[f"s{gg}"] = sol1
    if st.button("Calculate"):
        D = (e["a11"] * ((e["a22"] * e["a33"])-(e["a32"] * e["a23"]))) - (e["a12"] * ((e["a21"] * e["a33"])-(e["a31"] * e["a23"]))) + (e["a13"] * ((e["a21"] * e["a32"])-(e["a31"] * e["a22"])))
        Dx = (e["s1"] * ((e["a22"] * e["a33"])-(e["a32"] * e["a23"]))) - (e["a12"] * ((e["s2"] * e["a33"])-(e["s3"] * e["a23"]))) + (e["a13"] * ((e["s2"] * e["a32"])-(e["s3"] * e["a22"])))
        Dy = (e["a11"] * ((e["s2"] * e["a33"])-(e["s3"] * e["a23"]))) - (e["s1"] * ((e["a21"] * e["a33"])-(e["a31"] * e["a23"]))) + (e["a13"] * ((e["a21"] * e["s3"])-(e["a31"] * e["s2"])))
        Dz = (e["a11"] * ((e["a22"] * e["s3"])-(e["a32"] * e["s2"]))) - (e["a12"] * ((e["a21"] * e["s3"])-(e["a31"] * e["s2"]))) + (e["s1"] * ((e["a21"] * e["a32"])-(e["a31"] * e["a22"])))
        
        if Dx == 0 and Dy == 0 and Dz == 0 and D == 0:
            st.info("This Matrix has infinite solutions!")
            C = sp.Matrix([[e["a11"], e["a12"], e["a13"]], [e["a21"], e["a22"], e["a23"]], [e["a31"], e["a32"], e["a33"]]])
            S = sp.Matrix([e["s1"], e["s2"], e["s3"]])
            x, y, z = sp.symbols('x y z')
            st.success(f"{sp.linsolve((C, S), (x, y, z)).args[0]}")
        elif D == 0:
            st.error("No Solution")
        else:
            Dx, Dy, Dz = simp_frac([Dx, Dy, Dz], D)
                        
            st.success(f"({Dx}, {Dy}, {Dz})")
